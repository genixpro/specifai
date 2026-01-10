import { createFileRoute } from "@tanstack/react-router"

import { DataTable } from "@/elements/Common/DataTable"
import { columns, type UserTableData } from "@admin/elements/Admin/columns"

const defaultUsers: UserTableData[] = [
  {
    id: "user-1",
    email: "alex.johnson@example.com",
    full_name: "Alex Johnson",
    is_active: true,
    is_superuser: true,
    isCurrentUser: true,
  },
  {
    id: "user-2",
    email: "sam.taylor@example.com",
    full_name: "Sam Taylor",
    is_active: true,
    is_superuser: false,
    isCurrentUser: false,
  },
  {
    id: "user-3",
    email: "morgan.lee@example.com",
    full_name: null,
    is_active: false,
    is_superuser: false,
    isCurrentUser: false,
  },
]

const paginatedUsers: UserTableData[] = Array.from(
  { length: 12 },
  (_, index) => ({
    id: `user-${index + 1}`,
    email: `user${index + 1}@example.com`,
    full_name: index % 3 === 0 ? null : `User ${index + 1}`,
    is_active: index % 4 !== 0,
    is_superuser: index % 5 === 0,
    isCurrentUser: index === 0,
  }),
)

function UsersTableSnapshots() {
  return (
    <div className="min-h-screen bg-muted/30 p-8">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-10">
        <section className="space-y-3">
          <h1 className="text-xl font-semibold text-foreground">Default</h1>
          <div
            data-testid="users-table-default"
            className="rounded-lg border bg-background p-4 shadow-sm"
          >
            <DataTable columns={columns} data={defaultUsers} />
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-xl font-semibold text-foreground">Empty</h2>
          <div
            data-testid="users-table-empty"
            className="rounded-lg border bg-background p-4 shadow-sm"
          >
            <DataTable columns={columns} data={[]} />
          </div>
        </section>

        <section className="space-y-3">
          <h2 className="text-xl font-semibold text-foreground">Paginated</h2>
          <div
            data-testid="users-table-paginated"
            className="rounded-lg border bg-background p-4 shadow-sm"
          >
            <DataTable columns={columns} data={paginatedUsers} />
          </div>
        </section>
      </div>
    </div>
  )
}

export const Route = createFileRoute("/component-snapshots-users-table")({
  component: UsersTableSnapshots,
})
