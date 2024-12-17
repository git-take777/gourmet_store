import axios from 'axios';

// APIのベースURL
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// 認証関連のインターフェース
interface LoginCredentials {
  email: string;
  password: string;
}

interface RegisterData {
  email: string;
  password: string;
  username: string;
}

interface AuthResponse {
  access_token: string;
  token_type: string;
  user: {
    id: string;
    email: string;
    username: string;
  };
}

// ログイン関数
export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
  try {
    const response = await axios.post(`${API_URL}/auth/login`, credentials, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    
    // トークンをローカルストレージに保存
    if (response.data.access_token) {
      localStorage.setItem('auth_token', response.data.access_token);
    }
    
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Login failed');
  }
};

// 新規ユーザー登録関数
export const register = async (data: RegisterData): Promise<AuthResponse> => {
  try {
    const response = await axios.post(`${API_URL}/auth/register`, data, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Registration failed');
  }
};

// ログアウト関数
export const logout = async (): Promise<void> => {
  try {
    await axios.post(`${API_URL}/auth/logout`, {}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
      },
    });
    // ローカルストレージからトークンを削除
    localStorage.removeItem('auth_token');
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Logout failed');
  }
};

// 現在のユーザー情報を取得する関数
export const getCurrentUser = async (): Promise<AuthResponse['user']> => {
  try {
    const response = await axios.get(`${API_URL}/auth/me`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('auth_token')}`,
      },
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to get user info');
  }
};

// パスワードリセット要求を送信する関数
export const requestPasswordReset = async (email: string): Promise<void> => {
  try {
    await axios.post(`${API_URL}/auth/reset-password`, { email }, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Password reset request failed');
  }
};

// 認証トークンの有効性を確認する関数
export const verifyToken = async (): Promise<boolean> => {
  try {
    const token = localStorage.getItem('auth_token');
    if (!token) return false;
    
    const response = await axios.post(`${API_URL}/auth/verify-token`, {}, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.status === 200;
  } catch (error) {
    return false;
  }
};