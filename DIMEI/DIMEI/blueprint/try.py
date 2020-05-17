def get_signing_serializer(self, app):
    if not app.secret_key:
        return None
    signer_kwargs = dict(
        key_derivation=self.key_derivation,
        digest_method=self.digest_method
    )
    return URLSafeTimedSerializer(app.secret_key,
        salt=self.salt,
        serializer=self.serializer,
        signer_kwargs=signer_kwargs)