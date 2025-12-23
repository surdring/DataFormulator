import { zhCN } from "./zhCN";

// 当前仅支持中文，可在后续扩展为多语言（如 en-US）。
const currentLocale = "zh-CN" as const;

/**
 * 简单的文案获取函数：
 * - key 存在于 zhCN 中：返回对应中文；
 * - key 不存在：回退为 key 本身，方便在开发期发现遗漏。
 */
export const t = (key: string): string => {
  if (currentLocale === "zh-CN") {
    return zhCN[key] ?? key;
  }
  return key;
};

export type LocaleKey = keyof typeof zhCN;
export { zhCN };
