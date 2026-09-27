import { NextResponse, type NextRequest } from "next/server";

/**
 * Eenvoudige toegang voor het team via HTTP Basic Auth.
 * TEAM_USERS="naam:wachtwoord,naam2:wachtwoord2". Zonder TEAM_USERS staat de app open (alleen lokaal gebruiken).
 */
export function middleware(req: NextRequest) {
  if (req.nextUrl.pathname.startsWith("/api/cron/")) return NextResponse.next(); // eigen secret-check

  const users = (process.env.TEAM_USERS ?? "")
    .split(",")
    .map((u) => u.trim())
    .filter(Boolean);
  if (users.length === 0) return NextResponse.next();

  const header = req.headers.get("authorization");
  if (header?.startsWith("Basic ")) {
    const decoded = atob(header.slice(6));
    if (users.includes(decoded)) return NextResponse.next();
  }
  return new NextResponse("Inloggen vereist", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="ModernoMilano Backoffice", charset="UTF-8"' },
  });
}

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"] };
