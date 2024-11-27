import {post} from "@/utils/request";
import {USER_MODULE} from "@/api/_prefix";
import type {UserInfo} from "@/utils/types";

export const reqLogin = (loginInfo: UserInfo) => {
  return post<UserInfo>(`${USER_MODULE}/login`, loginInfo);
}

export const reqRegister = (registerInfo: UserInfo) => {
  return post<UserInfo>(`${USER_MODULE}/register`, registerInfo);
}