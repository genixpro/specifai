import type { CancelablePromise } from "@/utils/client"
import { OpenAPI } from "@/utils/client"
import { request } from "@/utils/client/core/request"

export type WorkspaceCreate = {
  name: string
}

export type WorkspacePublic = {
  id: string
  name: string
  owner_id: string
}

export type WorkspacesPublic = {
  data: WorkspacePublic[]
  count: number
}

export type WorkspacesReadData = {
  skip?: number
  limit?: number
}

export const readWorkspaces = (
  data: WorkspacesReadData = {},
): CancelablePromise<WorkspacesPublic> => {
  return request(OpenAPI, {
    method: "GET",
    url: "/api/v1/workspaces/",
    query: {
      skip: data.skip,
      limit: data.limit,
    },
  })
}

export const createWorkspace = (
  data: WorkspaceCreate,
): CancelablePromise<WorkspacePublic> => {
  return request(OpenAPI, {
    method: "POST",
    url: "/api/v1/workspaces/",
    body: data,
    mediaType: "application/json",
  })
}
