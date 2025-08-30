import apiClient from "@/utils/api-client";

export interface Post {
  userId: number;
  id: number;
  title: string;
  body: string;
}

const postApi = {
  getPosts: async (): Promise<Post[]> => {
    const { data } = await apiClient.get<Post[]>("/posts");
    return data;
  },
  getPost: async (id: number): Promise<Post> => {
    const { data } = await apiClient.get<Post>(`/posts/${id}`);
    return data;
  },
  createPost: async (post: Omit<Post, "id">): Promise<Post> => {
    const { data } = await apiClient.post<Post>("/posts", post);
    return data;
  },
};

export default postApi;
