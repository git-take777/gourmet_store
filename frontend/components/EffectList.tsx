'use client';

import { useEffect, useState } from 'react';
import { Box, Grid, Pagination, TextField, FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { useEffectStore } from '@/store/effectStore';
import { fetchEffects } from '@/services/api/effects';
import type { Effect } from '@/types/Effect';
import EffectCard from './EffectCard';
import Loading from '../Common/Loading';

const ITEMS_PER_PAGE = 12;

export default function EffectList() {
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [effectType, setEffectType] = useState('all');
  const [filteredEffects, setFilteredEffects] = useState<Effect[]>([]);
  
  const { effects, setEffects } = useEffectStore();

  // エフェクトデータの取得
  useEffect(() => {
    const loadEffects = async () => {
      try {
        const data = await fetchEffects();
        setEffects(data);
        setLoading(false);
      } catch (error) {
        console.error('Failed to fetch effects:', error);
        setLoading(false);
      }
    };
    loadEffects();
  }, [setEffects]);

  // フィルタリングとページネーションの処理
  useEffect(() => {
    let filtered = [...effects];

    // 検索フィルター
    if (search) {
      filtered = filtered.filter(effect => 
        effect.name.toLowerCase().includes(search.toLowerCase())
      );
    }

    // タイプフィルター
    if (effectType !== 'all') {
      filtered = filtered.filter(effect => 
        effect.type === effectType
      );
    }

    setFilteredEffects(filtered);
  }, [effects, search, effectType]);

  const pageCount = Math.ceil(filteredEffects.length / ITEMS_PER_PAGE);
  const displayedEffects = filteredEffects.slice(
    (page - 1) * ITEMS_PER_PAGE,
    page * ITEMS_PER_PAGE
  );

  if (loading) {
    return <Loading />;
  }

  return (
    <Box sx={{ padding: { xs: 2, md: 4 } }}>
      {/* フィルターコントロール */}
      <Box sx={{ 
        display: 'flex', 
        gap: 2, 
        marginBottom: 4,
        flexDirection: { xs: 'column', sm: 'row' } 
      }}>
        <TextField
          label="Search Effects"
          variant="outlined"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          sx={{ minWidth: 200 }}
        />
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Effect Type</InputLabel>
          <Select
            value={effectType}
            label="Effect Type"
            onChange={(e) => setEffectType(e.target.value)}
          >
            <MenuItem value="all">All Types</MenuItem>
            <MenuItem value="particle">Particle</MenuItem>
            <MenuItem value="sound">Sound</MenuItem>
            <MenuItem value="visual">Visual</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* エフェクトグリッド */}
      <Grid container spacing={3}>
        {displayedEffects.map((effect) => (
          <Grid item key={effect.id} xs={12} sm={6} md={4} lg={3}>
            <EffectCard effect={effect} />
          </Grid>
        ))}
      </Grid>

      {/* ページネーション */}
      {pageCount > 1 && (
        <Box sx={{ 
          display: 'flex', 
          justifyContent: 'center',
          marginTop: 4 
        }}>
          <Pagination
            count={pageCount}
            page={page}
            onChange={(_, value) => setPage(value)}
            color="primary"
          />
        </Box>
      )}
    </Box>
  );
}