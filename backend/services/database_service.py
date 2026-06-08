from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from models.report import Report

async def create_report(db: AsyncSession, title: str, content: str) -> Report:
    report = Report(title=title, content=content)
    db.add(report)
    await db.commit()
    await db.refresh(report)
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