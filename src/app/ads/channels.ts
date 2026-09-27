export const CHANNELS = [
  { id: "meta", label: "Meta (FB/IG)" },
  { id: "google", label: "Google" },
  { id: "tiktok", label: "TikTok" },
  { id: "pinterest", label: "Pinterest" },
  { id: "snapchat", label: "Snapchat" },
  { id: "influencers", label: "Influencers" },
  { id: "overig", label: "Overig" },
];

export const channelLabel = (id: string) => CHANNELS.find((c) => c.id === id)?.label ?? id;
