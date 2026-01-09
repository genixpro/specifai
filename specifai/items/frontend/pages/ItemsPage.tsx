import { useSuspenseQuery } from "@tanstack/react-query"
import { Search } from "lucide-react"
import { Suspense } from "react"

import { DataTable } from "@/elements/Common/DataTable"
import AddItem from "@items/elements/Items/AddItem"
import { columns } from "@items/elements/Items/columns"
import PendingItems from "@/elements/Pending/PendingItems"
import { readItems } from "@items/utils/itemsApi"
import { useWorkspaces } from "@workspaces/hooks/useWorkspaces"

function getItemsQueryOptions(workspaceId?: string | null) {
  return {
    queryFn: () =>
      readItems({ skip: 0, limit: 100, workspace_id: workspaceId }),
    queryKey: ["items", workspaceId],
  }
}

function ItemsTableContent() {
  const { activeWorkspaceId } = useWorkspaces()
  const { data: items } = useSuspenseQuery(
    getItemsQueryOptions(activeWorkspaceId),
  )

  if (items.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Search className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any items in this workspace yet
        </h3>
        <p className="text-muted-foreground">Add a new item to get started</p>
      </div>
    )
  }

  return <DataTable columns={columns} data={items.data} />
}

function ItemsTable() {
  return (
    <Suspense fallback={<PendingItems />}>
      <ItemsTableContent />
    </Suspense>
  )
}

export default function ItemsPage() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Items</h1>
          <p className="text-muted-foreground">Create and manage your items</p>
        </div>
        <AddItem />
      </div>
      <ItemsTable />
    </div>
  )
}
