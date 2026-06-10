from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.report import Report
print("DATABASE SERVICE LOADED")
async def add_report(db: AsyncSession, title: str, content: str) -> Report:
    print("1")
    report = Report(title=title, content=content)
    print("2")
    db.add(report)
    print("3")
    await db.commit()
    print("4")
    await db.refresh(report)
    print("5")
    return report

async def get_report(db: AsyncSession, report_id: int) -> Report | None:
    return await db.get(Report, report_id)

async def get_all_reports(db: AsyncSession) -> list[Report]:
    result = await db.execute(select(Report))
    return result.scalars().all()

async def delete_report(db: AsyncSession, report_id: int) -> bool:
    report = await db.get(Report, report_id)
    if not report:
        return False
    await db.delete(report)
    await db.commit()
    return True