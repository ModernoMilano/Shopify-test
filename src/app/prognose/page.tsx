import { PageHeader } from "@/components/PageHeader";
import { moneyNow } from "@/finance/data";
import { getFinanceSettings } from "@/finance/settings";
import { forecastSettings } from "@/finance/alerts";
import { ForecastView } from "./ForecastView";
import { day } from "@/components/ui";

export const dynamic = "force-dynamic";

export default async function ForecastPage() {
  const [s, money] = await Promise.all([getFinanceSettings(), moneyNow()]);
  const base = forecastSettings(s, money);
  return (
    <div className="mx-auto max-w-6xl">
      <PageHeader
        title="Prognose"
        subtitle={`Banksaldo dag voor dag vanaf ${day(base.startDate)}. Shopify betaalt alleen op werkdagen uit. Wijzigingen hier zijn om mee te rekenen, vaste instellingen staan bij Instellingen.`}
      />
      <ForecastView base={base} />
    </div>
  );
}
