import { PageHeader } from "@/components/PageHeader";
import { AdSwiper } from "./AdSwiper";
import data from "./ads.json";
import type { Ad } from "./types";

export const metadata = { title: "Ads swipen · ModernoMilano Backoffice" };

export default function AdsPage() {
  const ads = data as Ad[];
  return (
    <div className="mx-auto max-w-6xl">
      <PageHeader
        title="Ads swipen"
        subtitle={`${ads.length} ModernoMilano-beelden uit Higgsfield, elk met eigen copy, angle en hook. Rechts is plaatsen, links is overslaan.`}
      />
      <AdSwiper ads={ads} />
    </div>
  );
}
