import axios from 'axios';
import { Effect } from '@/types/Effect';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

/**
 * エフェクトに関するAPI呼び出しを管理するクラス
 */
export class EffectsAPI {
  /**
   * 全てのエフェクトを取得
   * @returns Promise<Effect[]>
   */
  static async getAllEffects(): Promise<Effect[]> {
    try {
      const response = await axios.get<Effect[]>(`${API_BASE_URL}/api/magic-effects`);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch effects:', error);
      throw error;
    }
  }

  /**
   * 特定のエフェクトを取得
   * @param id エフェクトID
   * @returns Promise<Effect>
   */
  static async getEffectById(id: string): Promise<Effect> {
    try {
      const response = await axios.get<Effect>(`${API_BASE_URL}/api/magic-effects/${id}`);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch effect with id ${id}:`, error);
      throw error;
    }
  }

  /**
   * 新しいエフェクトを作成
   * @param effect 作成するエフェクトのデータ
   * @returns Promise<Effect>
   */
  static async createEffect(effect: Omit<Effect, 'id'>): Promise<Effect> {
    try {
      const response = await axios.post<Effect>(`${API_BASE_URL}/api/magic-effects`, effect);
      return response.data;
    } catch (error) {
      console.error('Failed to create effect:', error);
      throw error;
    }
  }

  /**
   * エフェクトを更新
   * @param id エフェクトID
   * @param effect 更新するエフェクトのデータ
   * @returns Promise<Effect>
   */
  static async updateEffect(id: string, effect: Partial<Effect>): Promise<Effect> {
    try {
      const response = await axios.put<Effect>(`${API_BASE_URL}/api/magic-effects/${id}`, effect);
      return response.data;
    } catch (error) {
      console.error(`Failed to update effect with id ${id}:`, error);
      throw error;
    }
  }

  /**
   * エフェクトを削除
   * @param id エフェクトID
   * @returns Promise<void>
   */
  static async deleteEffect(id: string): Promise<void> {
    try {
      await axios.delete(`${API_BASE_URL}/api/magic-effects/${id}`);
    } catch (error) {
      console.error(`Failed to delete effect with id ${id}:`, error);
      throw error;
    }
  }
}

/**
 * SWRのフェッチャー関数
 */
export const effectsFetcher = async (url: string) => {
  const response = await axios.get(url);
  return response.data;
};

/**
 * エラーハンドリング用のユーティリティ関数
 */
export const handleApiError = (error: any) => {
  if (axios.isAxiosError(error)) {
    return {
      message: error.response?.data?.message || 'An unexpected error occurred',
      status: error.response?.status || 500
    };
  }
  return {
    message: 'An unexpected error occurred',
    status: 500
  };
};