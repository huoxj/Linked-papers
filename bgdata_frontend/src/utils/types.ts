export type PaperContent = {
  title: string;
  abstract: string;
  year: string;
  category: string;
  refCount: number;
}

/**
 * USER_MODULE: 用户模块
 */

export type UserInfo = {
  email: string;
  username?: string;
  password: string;
  premium?: boolean;
}

/**
 * PAPER_MODULE: 论文模块
 */

export type Text = {
  text: string;
}

/**
 * SERVICE_MODULE: 服务模块
 */

export type SearchResult = {
  idList: number[];
  totalPage: number;
}