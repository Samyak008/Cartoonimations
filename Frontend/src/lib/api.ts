import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface AnimationResponse {
  video_path: string;
  audio_path: string;
  message: string;
  status: string;
}

export const api = {
  /**
   * Check if the API server is running
   */
  healthCheck: async (): Promise<{ status: string; message: string }> => {
    const response = await apiClient.get('/health');
    return response.data;
  },

  /**
   * Generate an educational animation from a prompt
   */
  generateAnimation: async (prompt: string): Promise<AnimationResponse> => {
    const response = await apiClient.post('/generate', { prompt });
    return response.data;
  },
};

export default api;