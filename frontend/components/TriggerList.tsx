'use client';

import { useEffect, useState } from 'react';
import { Box, Typography, Card, CardContent, Grid, CircularProgress } from '@mui/material';
import axios from 'axios';
import useSWR from 'swr';

// トリガーのインターフェース定義
interface Trigger {
  id: string;
  name: string;
  type: string;
  condition: {
    type: string;
    value: any;
  };
  enabled: boolean;
  created_at: string;
}

// トリガーフェッチャー関数
const fetchTriggers = async () => {
  const response = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/triggers`);
  return response.data;
};

// トリガーカードコンポーネント
const TriggerCard = ({ trigger }: { trigger: Trigger }) => (
  <Card 
    sx={{ 
      height: '100%',
      transition: 'transform 0.2s',
      '&:hover': {
        transform: 'scale(1.02)',
      }
    }}
  >
    <CardContent>
      <Typography variant="h6" component="div" gutterBottom>
        {trigger.name}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Type: {trigger.type}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        Status: {trigger.enabled ? 'Enabled' : 'Disabled'}
      </Typography>
      <Typography variant="caption" display="block">
        Created: {new Date(trigger.created_at).toLocaleDateString()}
      </Typography>
    </CardContent>
  </Card>
);

// メインのトリガーリストコンポーネント
export default function TriggerList() {
  const { data: triggers, error, isLoading } = useSWR<Trigger[]>(
    'triggers',
    fetchTriggers,
    {
      refreshInterval: 5000, // 5秒ごとに更新
    }
  );

  if (error) {
    return (
      <Box sx={{ p: 3, textAlign: 'center' }}>
        <Typography color="error">
          Error loading triggers. Please try again later.
        </Typography>
      </Box>
    );
  }

  if (isLoading) {
    return (
      <Box sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '200px' 
      }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ p: { xs: 2, md: 3 } }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Triggers
      </Typography>
      <Grid container spacing={3}>
        {triggers?.map((trigger) => (
          <Grid item xs={12} sm={6} md={4} key={trigger.id}>
            <TriggerCard trigger={trigger} />
          </Grid>
        ))}
        {triggers?.length === 0 && (
          <Grid item xs={12}>
            <Typography variant="body1" textAlign="center">
              No triggers found. Create your first trigger to get started.
            </Typography>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}

// パフォーマンス最適化のためのメモ化
TriggerList.whyDidYouRender = true;