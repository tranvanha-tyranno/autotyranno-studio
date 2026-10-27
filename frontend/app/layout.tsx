import type { Metadata } from "next";
import "./base.css";

export const metadata: Metadata = { title: "AutoTyranno · Video Studio", description: "Quản lý quy trình tạo video sản phẩm với Muse, Gemini và Adam V3" };

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="vi"><body>{children}</body></html>;
}
