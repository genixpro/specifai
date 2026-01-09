import { useQuery } from "@tanstack/react-query"
import { useEffect, useMemo, useState } from "react"

import { readWorkspaces } from "@workspaces/utils/workspaceApi"

const ACTIVE_WORKSPACE_KEY = "active_workspace_id"

export const useWorkspaces = () => {
  const { data, isLoading } = useQuery({
    queryKey: ["workspaces"],
    queryFn: () => readWorkspaces({ skip: 0, limit: 100 }),
  })
  const [activeWorkspaceId, setActiveWorkspaceIdState] = useState<
    string | null
  >(() => localStorage.getItem(ACTIVE_WORKSPACE_KEY))

  useEffect(() => {
    if (!activeWorkspaceId && data?.data?.length) {
      const nextId = data.data[0].id
      setActiveWorkspaceIdState(nextId)
      localStorage.setItem(ACTIVE_WORKSPACE_KEY, nextId)
    }
  }, [activeWorkspaceId, data])

  const setActiveWorkspaceId = (id: string) => {
    setActiveWorkspaceIdState(id)
    localStorage.setItem(ACTIVE_WORKSPACE_KEY, id)
  }

  const activeWorkspace = useMemo(() => {
    return data?.data?.find((workspace) => workspace.id === activeWorkspaceId)
  }, [activeWorkspaceId, data])

  return {
    workspaces: data?.data ?? [],
    activeWorkspace,
    activeWorkspaceId,
    setActiveWorkspaceId,
    isLoading,
  }
}
