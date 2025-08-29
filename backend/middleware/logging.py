import json
import logging
import os
import time
from typing import Callable
from uuid import uuid4

import logging_loki
import requests
import yaml
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse
from requests import RequestException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message

from backend.helpers.constants import PROJECT_PATH
from backend.helpers.utility import AsyncIteratorWrapper

load_dotenv(os.environ.get('ENV_PATH'))


class LoggingMiddleware(BaseHTTPMiddleware):

    def __init__(
            self,
            app: FastAPI,
            *,
            logger: logging.Logger
    ) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(self,
                       request: Request,
                       call_next: Callable
                       ) -> Response:
        request_id: str = str(uuid4())
        logging_dict = {
            "X-API-REQUEST-ID": request_id
        }

        await self.set_body(request)
        response, response_dict = await self._log_response(call_next,
                                                           request,
                                                           request_id
                                                           )
        request_dict = await self._log_request(request)
        logging_dict["request"] = request_dict
        logging_dict["response"] = response_dict

        self._logger.info(logging_dict)

        return response

    async def set_body(self, request: Request):
        body = await request.body()
        request._body = body

        async def receive() -> Message:
            return {
                "type": "http.request",
                "body": body,
                "more_body": False
            }

        request._receive = receive

    async def _log_request(
            self,
            request: Request
    ) -> str:

        path = request.url.path
        if request.query_params:
            path += f"?{request.query_params}"

        request_logging = {
            "method": request.method,
            "path": path,
            "ip": request.client.host
        }

        try:
            body = await request.json()
            request_logging["body"] = body
        except Exception:
            try:
                request_logging["body"] = request._body.decode()
            except Exception:
                request_logging["body"] = "[Unreadable body]"

        return request_logging

    async def _log_response(self,
                            call_next: Callable,
                            request: Request,
                            request_id: str
                            ) -> Response:

        start_time = time.perf_counter()
        response = await self._execute_request(call_next, request, request_id)
        finish_time = time.perf_counter()

        overall_status = "successful" if response.status_code < 400 else "failed"
        execution_time = finish_time - start_time

        response_logging = {
            "status": overall_status,
            "status_code": response.status_code,
            "time_taken": f"{execution_time:0.4f}s"
        }

        try:
            resp_body = [section async for section in response.__dict__["body_iterator"]]
            response.__setattr__("body_iterator", AsyncIteratorWrapper(resp_body))

            raw_body = resp_body[0] if resp_body else b""
            content_type = response.headers.get("content-type", "").lower()

            if "application/json" in content_type:
                try:
                    decoded = raw_body.decode("utf-8", errors="replace")
                    parsed = json.loads(decoded)
                    response_logging["body"] = parsed
                except Exception:
                    response_logging["body"] = decoded[:300] + "... [invalid JSON or truncated]"

            elif "text/html" in content_type:
                response_logging["body"] = "[HTML response omitted]"

            elif "image" in content_type or b"\x89PNG" in raw_body or b"\xFF\xD8" in raw_body:
                response_logging["body"] = f"[Binary image response of {len(raw_body)} bytes]"

            else:
                decoded = raw_body.decode("utf-8", errors="replace")
                response_logging["body"] = decoded[:300] + ("..." if len(decoded) > 300 else "")

        except Exception as e:
            response_logging["body"] = f"[Could not read response body: {str(e)}]"

        return response, response_logging

    async def _execute_request(self,
                               call_next: Callable,
                               request: Request,
                               request_id: str
                               ) -> Response:
        try:
            response: Response = await call_next(request)

            response.headers["X-API-Request-ID"] = request_id
            return response

        except Exception as e:
            self._logger.exception(
                {
                    "path": request.url.path,
                    "method": request.method,
                    "reason": e
                }
            )
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Internal Server Error"}
            )


class DefaultTagsFilter(logging.Filter):
    def __init__(self, tags):
        super().__init__()
        self.tags = tags

    def filter(self, record):
        if not hasattr(record, 'tags'):
            record.tags = self.tags
        else:
            # If there's already a 'tags' attribute, update it with default tags.
            # This avoids overriding any custom tags set at the log call.
            record.tags.update(self.tags)
        return True


def init_logging(name):
    with open(os.path.join(PROJECT_PATH,"backend", "config", "app-logging.yaml"), 'rb') as f:
        log_config = yaml.load(f.read(), Loader=yaml.FullLoader)
    logging.config.dictConfig(log_config)
    return configure_logger_for_loki(logging.getLogger(name))


def configure_logger_for_loki(logger):
    try:
        loki_url = os.getenv('LOKI_BACKEND')
        service_tag = os.getenv('SERVICE_TAG')

        if is_loki_available(loki_url):
            logging_loki.emitter.LokiEmitter.level_tag = "level"
            # assign to a variable named handler
            handler = logging_loki.LokiHandler(
                url=loki_url + "/loki/api/v1/push",
                version="1",
            )
            tags_filter = DefaultTagsFilter(
                {"service": service_tag})
            handler.addFilter(tags_filter)
            logger.addHandler(handler)
    except Exception as e:
        logger.error("Error in setting up Loki logging backend: {}".format(str(e)))
        logger.error("Continuing with default logging backend")

    return logger


def is_loki_available(LOKI_URL: str) -> bool:
    try:
        response = requests.get(f"{LOKI_URL}/ready", timeout=3)
        return response.status_code == status.HTTP_200_OK
    except RequestException:
        return False


app_logger = init_logging(__name__)
