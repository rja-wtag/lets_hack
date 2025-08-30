import { useEffect, useState } from "react";
import postApi, { type Post } from "@/api/post-api";
import { Card, CardContent, CardDescription, CardTitle } from "./ui/card";

function Posts() {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    postApi.getPosts().then(setPosts).catch(console.error);
  }, []);

  return (
    <div>
      <h1 className="text-xl font-bold mb-4">Posts</h1>
      {posts.map((post) => (
        <Card key={post.id} className="mb-3 shadow-md">
          <CardContent>
            <CardTitle>{post.title}</CardTitle>
            <CardDescription>{post.body}</CardDescription>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export default Posts;
