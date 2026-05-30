import strawberry
from typing import Optional, List
from datetime import datetime

_tasks = [
    {"id": 1, "title": "Set up CI pipeline", "status": "done", "priority": "high", "created_at": "2026-05-01"},
    {"id": 2, "title": "Write unit tests", "status": "in_progress", "priority": "medium", "created_at": "2026-05-10"},
    {"id": 3, "title": "Deploy to staging", "status": "pending", "priority": "high", "created_at": "2026-05-15"},
]
_next_id = 4

@strawberry.type
class Task:
    id: int
    title: str
    status: str
    priority: str
    created_at: str

@strawberry.type
class DeleteResult:
    success: bool
    message: str

@strawberry.type
class Query:
    @strawberry.field
    def tasks(self, status: Optional[str] = None) -> List[Task]:
        result = _tasks
        if status:
            result = [t for t in _tasks if t["status"] == status]
        return [Task(**t) for t in result]

    @strawberry.field
    def task(self, id: int) -> Optional[Task]:
        match = next((t for t in _tasks if t["id"] == id), None)
        return Task(**match) if match else None

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_task(
        self,
        title: str,
        status: Optional[str] = "pending",
        priority: Optional[str] = "medium",
    ) -> Task:
        global _next_id
        task = {
            "id": _next_id,
            "title": title,
            "status": status,
            "priority": priority,
            "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
        }
        _tasks.append(task)
        _next_id += 1
        return Task(**task)

    @strawberry.mutation
    def update_task(
        self,
        id: int,
        title: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Optional[Task]:
        task = next((t for t in _tasks if t["id"] == id), None)
        if not task:
            return None
        if title is not None:
            task["title"] = title
        if status is not None:
            task["status"] = status
        if priority is not None:
            task["priority"] = priority
        return Task(**task)

    @strawberry.mutation
    def delete_task(self, id: int) -> DeleteResult:
        task = next((t for t in _tasks if t["id"] == id), None)
        if not task:
            return DeleteResult(success=False, message=f"task {id} not found")
        _tasks.remove(task)
        return DeleteResult(success=True, message=f"task {id} deleted")

schema = strawberry.Schema(query=Query, mutation=Mutation)
