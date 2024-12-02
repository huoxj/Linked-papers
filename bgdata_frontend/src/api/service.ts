import  {get} from "@/utils/request";
import {SERVICE_MODULE} from "@/api/_prefix";
import type {SearchResult} from "@/utils/types";

export const reqSearch = (param: {key: string; page: number}) => {
  return get<SearchResult>(`${SERVICE_MODULE}/search`, param)
}

export const reqRecommend = () => {
  return get<number[]>(`${SERVICE_MODULE}/recommend`)
}