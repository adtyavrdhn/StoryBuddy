# # apps/users/api/v1/schemas.py
# from ninja import Schema
# from pydantic import EmailStr


# class TokenSchema(Schema):
#     access_token: str
#     refresh_token: str


# class AuthLoginSchema(Schema):
#     email: EmailStr
#     password: str


# class AuthOut(Schema):
#     token: TokenSchema
#     message: str


# class RefreshSchema(Schema):
#     refresh_token: str
