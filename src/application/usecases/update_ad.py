from dataclasses import asdict

from src.application.exceptions import AdNotFoundError, ForbiddenError
from src.application.ports.uow import UnitOfWork
from src.application.ports.usecases import UpdateAdPort
from src.domain.entities import Ad, AdStatus


class UpdateAd(UpdateAdPort):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(
            self,
            ad_id: int,
            user_id: int,
            title: str | None,
            description: str | None,
            price: int | None,
            category: str | None,
            city: str | None,
    ) -> Ad:
        async with self._uow as u:
            ad = await u.ads.get_by_id(ad_id)
            if not ad or ad.status == AdStatus.ARCHIVED:
                raise AdNotFoundError
            if ad.user_id != user_id:
                raise ForbiddenError
            args = locals()
            for key,value in args.items():
                if value is None:
                    args[key] = asdict(ad)[key]
            ad.edit(args['title'], args['description'], args['price'], args['category'], args['city'])
            await self._uow.ads.save(ad)
            await self._uow.outbox.add('ad.updated', payload={'ad_id': ad.id})
            await self._uow.commit()
            return ad
