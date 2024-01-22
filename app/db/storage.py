import aiosqlite


class Database:
    def __init__(self, connection: aiosqlite.Connection):
        self.db: aiosqlite.Connection = connection

    async def create_users_table(self):
        await self.db.execute(sql="""CREATE TABLE IF NOT EXISTS users(
                        id INTEGER PRIMARY KEY,
                        tg_id BIGINT,
                        name VARCHAR(30),
                        phone VARCHAR(20),
                        city VARCHAR(30),
                        uniq_code VARCHAR(10)
        )""")

    async def check_exist_user(self, user_id):
        user = await self.db.execute(sql="SELECT id FROM users WHERE tg_id=?", parameters=(user_id,))
        data = await user.fetchone()

        return True if not data else False

    async def register_user(self, user_id, name):
        if await self.check_exist_user(user_id=user_id):
            await self.db.execute(sql="INSERT INTO users(tg_id, name) VALUES(?, ?)", parameters=(user_id, name,))
            await self.db.commit()

            return True
        return None

    async def check_phone(self, user_id):
        phone = await self.db.execute(sql="SELECT phone FROM users WHERE tg_id=?", parameters=(user_id,))
        data = await phone.fetchone()

        return data[0]

    async def insert_phone(self, user_id, phone):
        if not await self.check_phone(user_id=user_id):
            await self.db.execute(sql="UPDATE users SET phone=? WHERE tg_id=?", parameters=(phone, user_id,))
            await self.db.commit()

            return True
        return None

    async def insert_city(self, user_id, city):
        await self.db.execute(sql="UPDATE users SET city=? WHERE tg_id=?", parameters=(city, user_id,))
        await self.db.commit()

        return True

    async def check_code(self, user_id):
        code = await self.db.execute(sql="SELECT uniq_code FROM users WHERE tg_id=?", parameters=(user_id,))
        data = await code.fetchone()

        return data[0]

    async def insert_code(self, user_id, code):
        if not await self.check_code(user_id=user_id):
            await self.db.execute(sql="UPDATE users SET uniq_code=? WHERE tg_id=?", parameters=(code, user_id,))
            await self.db.commit()

            return True
        return None

    async def get_all_codes(self):
        request = await self.db.execute(sql="SELECT uniq_code FROM users")
        codes = [code[0] for code in await request.fetchall()]

        return codes
