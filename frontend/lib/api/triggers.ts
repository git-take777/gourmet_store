import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

interface TriggerPayload {
  effectId: string;
  parameters?: {
    intensity?: number;
    duration?: number;
    color?: string;
    [key: string]: any;
  };
}

interface TriggerResponse {
  success: boolean;
  triggerId: string;
  timestamp: string;
  message?: string;
}

/**
 * トリガーを作成する
 * @param payload トリガーのペイロード
 * @returns トリガーのレスポンス
 */
export const createTrigger = async (payload: TriggerPayload): Promise<TriggerResponse> => {
  try {
    const response = await axios.post(`${API_URL}/api/triggers`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error creating trigger:', error);
    throw error;
  }
};

/**
 * トリガーを取得する
 * @param triggerId トリガーID
 * @returns トリガーの情報
 */
export const getTrigger = async (triggerId: string): Promise<TriggerResponse> => {
  try {
    const response = await axios.get(`${API_URL}/api/triggers/${triggerId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching trigger:', error);
    throw error;
  }
};

/**
 * トリガーをキャンセルする
 * @param triggerId トリガーID
 * @returns キャンセル結果
 */
export const cancelTrigger = async (triggerId: string): Promise<TriggerResponse> => {
  try {
    const response = await axios.delete(`${API_URL}/api/triggers/${triggerId}`);
    return response.data;
  } catch (error) {
    console.error('Error canceling trigger:', error);
    throw error;
  }
};

/**
 * トリガーの一覧を取得する
 * @param limit 取得する件数
 * @param offset オフセット
 * @returns トリガーの一覧
 */
export const listTriggers = async (
  limit: number = 10,
  offset: number = 0
): Promise<{ triggers: TriggerResponse[]; total: number }> => {
  try {
    const response = await axios.get(`${API_URL}/api/triggers`, {
      params: { limit, offset },
    });
    return response.data;
  } catch (error) {
    console.error('Error listing triggers:', error);
    throw error;
  }
};

/**
 * トリガーを更新する
 * @param triggerId トリガーID
 * @param payload 更新するペイロード
 * @returns 更新結果
 */
export const updateTrigger = async (
  triggerId: string,
  payload: Partial<TriggerPayload>
): Promise<TriggerResponse> => {
  try {
    const response = await axios.put(`${API_URL}/api/triggers/${triggerId}`, payload, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error updating trigger:', error);
    throw error;
  }
};