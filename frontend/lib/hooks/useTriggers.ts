import { useState, useCallback } from 'react';
import { useSWR } from 'swr';
import axios from 'axios';

// トリガーの型定義
interface Trigger {
  id: string;
  name: string;
  condition: string;
  effectId: string;
  isActive: boolean;
  parameters: Record<string, unknown>;
}

// トリガー作成のための入力型
interface CreateTriggerInput {
  name: string;
  condition: string;
  effectId: string;
  parameters?: Record<string, unknown>;
}

// APIエンドポイントの設定
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;
const TRIGGERS_ENDPOINT = `${API_BASE_URL}/api/triggers`;

/**
 * トリガー関連の操作を管理するカスタムフック
 * @returns トリガー関連の操作と状態を提供するオブジェクト
 */
export const useTriggers = () => {
  const [error, setError] = useState<Error | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // SWRを使用してトリガー一覧を取得
  const { data: triggers, mutate } = useSWR<Trigger[]>(
    TRIGGERS_ENDPOINT,
    async (url) => {
      const response = await axios.get(url);
      return response.data;
    }
  );

  // トリガーの作成
  const createTrigger = useCallback(async (input: CreateTriggerInput) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post(TRIGGERS_ENDPOINT, input);
      await mutate(); // データを再取得
      return response.data;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  // トリガーの更新
  const updateTrigger = useCallback(async (id: string, updates: Partial<CreateTriggerInput>) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.put(`${TRIGGERS_ENDPOINT}/${id}`, updates);
      await mutate(); // データを再取得
      return response.data;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  // トリガーの削除
  const deleteTrigger = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await axios.delete(`${TRIGGERS_ENDPOINT}/${id}`);
      await mutate(); // データを再取得
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  // トリガーの有効/無効切り替え
  const toggleTrigger = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await axios.post(`${TRIGGERS_ENDPOINT}/${id}/toggle`);
      await mutate(); // データを再取得
      return response.data;
    } catch (err) {
      setError(err as Error);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [mutate]);

  return {
    triggers,
    isLoading,
    error,
    createTrigger,
    updateTrigger,
    deleteTrigger,
    toggleTrigger,
    refreshTriggers: mutate
  };
};

export default useTriggers;
const MyComponent = () => {
  const { 
    triggers, 
    isLoading, 
    error, 
    createTrigger 
  } = useTriggers();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      {triggers?.map(trigger => (
        <div key={trigger.id}>{trigger.name}</div>
      ))}
    </div>
  );
};