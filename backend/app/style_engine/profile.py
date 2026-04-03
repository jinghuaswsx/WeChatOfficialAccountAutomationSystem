from __future__ import annotations
import json
from sqlalchemy.orm import Session
from backend.app.models.style_profile import StyleProfile


class StyleProfileManager:
    def __init__(self, db_session: Session) -> None:
        self._session = db_session

    def save(self, features: dict) -> StyleProfile:
        latest = self._session.query(StyleProfile).order_by(StyleProfile.version.desc()).first()
        new_version = (latest.version + 1) if latest else 1
        profile = StyleProfile(version=new_version, features_json=json.dumps(features, ensure_ascii=False))
        self._session.add(profile)
        self._session.commit()
        return profile

    def get_latest(self) -> dict | None:
        latest = self._session.query(StyleProfile).order_by(StyleProfile.version.desc()).first()
        if latest is None:
            return None
        return json.loads(latest.features_json)
