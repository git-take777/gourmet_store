import useSWR from 'swr';
import { useCallback } from 'react';
import { Effect } from '../types/Effect';
import { fetchEffects } from '../api/effects';
import { useEffectStore } from '../store/effectStore';

/**
 * エフェクトの一覧を取得するカスタムフック
 * @returns エフェクト一覧とローディング・エラー状態
 */
export const useEffectsList = () => {
  const { data, error, mutate } = useSWR<Effect[]>('/api/effects', fetchEffects, {
    revalidateOnFocus: false,
    revalidateOnReconnect: true,
  });

  const setEffects = useEffectStore((state) => state.setEffects);

  // データが更新されたらストアも更新
  if (data) {
    setEffects(data);
  }

  return {
    effects: data,
    isLoading: !error && !data,
    isError: error,
    mutate,
  };
};

/**
 * 特定のエフェクトを取得するカスタムフック
 * @param id エフェクトID
 * @returns 特定のエフェクトとローディング・エラー状態
 */
export const useEffect = (id: string) => {
  const { data, error } = useSWR<Effect>(
    id ? `/api/effects/${id}` : null,
    async () => {
      const response = await fetch(`/api/effects/${id}`);
      if (!response.ok) throw new Error('Failed to fetch effect');
      return response.json();
    }
  );

  return {
    effect: data,
    isLoading: !error && !data,
    isError: error,
  };
};

/**
 * エフェクトを追加するカスタムフック
 * @returns エフェクト追加関数
 */
export const useAddEffect = () => {
  const addEffect = useEffectStore((state) => state.addEffect);
  const { mutate: mutateEffects } = useEffectsList();

  const addNewEffect = useCallback(
    async (effect: Omit<Effect, 'id'>) => {
      try {
        const response = await fetch('/api/effects', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(effect),
        });

        if (!response.ok) {
          throw new Error('Failed to add effect');
        }

        const newEffect = await response.json();
        addEffect(newEffect);
        await mutateEffects();
        return newEffect;
      } catch (error) {
        console.error('Error adding effect:', error);
        throw error;
      }
    },
    [addEffect, mutateEffects]
  );

  return { addNewEffect };
};

/**
 * エフェクトのパラメータを更新するカスタムフック
 * @returns エフェクト更新関数
 */
export const useUpdateEffectParameters = () => {
  const { mutate: mutateEffects } = useEffectsList();

  const updateParameters = useCallback(
    async (id: string, parameters: Effect['parameters']) => {
      try {
        const response = await fetch(`/api/effects/${id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ parameters }),
        });

        if (!response.ok) {
          throw new Error('Failed to update effect parameters');
        }

        await mutateEffects();
        return await response.json();
      } catch (error) {
        console.error('Error updating effect parameters:', error);
        throw error;
      }
    },
    [mutateEffects]
  );

  return { updateParameters };
};