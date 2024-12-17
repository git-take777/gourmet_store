'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { styled } from '@mui/material/styles';
import {
  AppBar,
  Toolbar,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemText,
  Box,
  useMediaQuery,
  useTheme,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

// スタイル付きコンポーネントの定義
const StyledNav = styled('nav')(({ theme }) => ({
  width: '100%',
  backgroundColor: theme.palette.background.paper,
}));

const NavLink = styled(Link)(({ theme }) => ({
  color: theme.palette.text.primary,
  textDecoration: 'none',
  padding: theme.spacing(2),
  '&:hover': {
    color: theme.palette.primary.main,
  },
}));

// ナビゲーションアイテムの定義
const navItems = [
  { title: 'Home', path: '/' },
  { title: 'Effects', path: '/effects' },
  { title: 'Dashboard', path: '/dashboard' },
];

const Navigation = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const pathname = usePathname();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  // モバイル用のドロワーメニュー
  const drawer = (
    <Box onClick={handleDrawerToggle}>
      <List>
        {navItems.map((item) => (
          <ListItem
            key={item.path}
            component={Link}
            href={item.path}
            selected={pathname === item.path}
          >
            <ListItemText primary={item.title} />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  // デスクトップ用のナビゲーション
  const desktopNav = (
    <Box sx={{ display: 'flex', gap: 2 }}>
      {navItems.map((item) => (
        <NavLink
          key={item.path}
          href={item.path}
          aria-current={pathname === item.path ? 'page' : undefined}
        >
          {item.title}
        </NavLink>
      ))}
    </Box>
  );

  return (
    <StyledNav>
      <AppBar position="static" color="default" elevation={1}>
        <Toolbar>
          {isMobile && (
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2 }}
            >
              <MenuIcon />
            </IconButton>
          )}
          
          {/* ロゴ部分 */}
          <Box sx={{ flexGrow: 1 }}>
            <Link href="/" passHref>
              <Box component="span" sx={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                GrubTrack
              </Box>
            </Link>
          </Box>

          {/* デスクトップナビゲーション */}
          {!isMobile && desktopNav}
        </Toolbar>
      </AppBar>

      {/* モバイルドロワー */}
      {isMobile && (
        <Drawer
          variant="temporary"
          anchor="left"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // モバイルでのパフォーマンス向上のため
          }}
        >
          {drawer}
        </Drawer>
      )}
    </StyledNav>
  );
};

export default Navigation;
// Layout.tsxなどで
import Navigation from '@/components/Navigation';

export default function Layout({ children }) {
  return (
    <>
      <Navigation />
      <main>{children}</main>
    </>
  );
}