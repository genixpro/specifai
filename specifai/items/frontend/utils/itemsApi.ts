import type { CancelablePromise, ItemCreate, ItemsPublic } from "@/utils/client"
import { OpenAPI } from "@/utils/client"
import { request } from "@/utils/client/core/request"

export type ItemCreateWithWorkspace = ItemCreate & {
  workspace_id?: string | null
}

export type ItemsReadData = {
  skip?: number
  limit?: number
  workspace_id?: string | null
}

export const readItems = (
  data: ItemsReadData = {},
): CancelablePromise<ItemsPublic> => {
  return request(OpenAPI, {
    method: "GET",
    url: "/api/v1/items/",
    query: {
      skip: data.skip,
      limit: data.limit,
      workspace_id: data.workspace_id ?? undefined,
    },
  })
}

export const createItem = (
  data: ItemCreateWithWorkspace,
): CancelablePromise<ItemsPublic["data"][number]> => {
  return request(OpenAPI, {
    method: "POST",
    url: "/api/v1/items/",
    body: data,
    mediaType: "application/json",
  })
}
