import { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { AuthProvider } from '@/contexts/AuthContext'
import Layout from '@/components/Layout'
import '@/styles/globals.css'

// Interフォントの設定
const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
})

// メタデータの設定
export const metadata: Metadata = {
  title: {
    template: '%s | GrubTrack',
    default: 'GrubTrack - Minecraft Effect Management System',
  },
  description: 'Professional Minecraft effect management and tracking system',
  keywords: ['minecraft', 'effects', 'management', 'tracking', 'gaming'],
  authors: [{ name: 'GrubTrack Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: process.env.NEXT_PUBLIC_SITE_URL,
    siteName: 'GrubTrack',
    images: [
      {
        url: '/og-image.png',
        width: 1200,
        height: 630,
        alt: 'GrubTrack',
      },
    ],
  },
}

// ルートレイアウトの型定義
interface RootLayoutProps {
  children: React.ReactNode;
}

// ルートレイアウトコンポーネント
export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className={inter.className}>
      <body>
        <AuthProvider>
          {/* 
            Layoutコンポーネントでヘッダー、フッター、サイドバーを含む
            全体的なページ構造を提供
          */}
          <Layout>
            <main className="min-h-screen w-full">
              {/* 
                コンテンツエリア
                レスポンシブデザインのためのクラスを適用
              */}
              <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {children}
              </div>
            </main>
          </Layout>
        </AuthProvider>

        {/* 
          開発環境でのデバッグツール
          本番環境では除外される
        */}
        {process.env.NODE_ENV === 'development' && (
          <div id="debug-panel" />
        )}
      </body>
    </html>
  );
}

// キャッシュの設定
export const revalidate = 3600; // 1時間

// 動的レンダリングの設定
export const dynamic = 'force-dynamic';

// ランタイムの設定
export const runtime = 'nodejs';