import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
    // Create categories
    const fruitsCategory = await prisma.category.create({
        data: {
            name: 'Fruits',
            order: 1,
        },
    });

    const vegetablesCategory = await prisma.category.create({
        data: {
            name: 'Vegetables',
            order: 2,
        },
    });

    // Create items
    await prisma.item.createMany({
        data: [
            {
                name: 'Apple',
                is_active: true,
                quantity: 10,
                unit: 'kg',
                category_id: fruitsCategory.id,
            },
            {
                name: 'Banana',
                is_active: true,
                quantity: 5,
                unit: 'kg',
                category_id: fruitsCategory.id,
            },
            {
                name: 'Carrot',
                is_active: false,
                quantity: 7,
                unit: 'kg',
                category_id: vegetablesCategory.id,
            },
        ],
    });

    // Create a user
    const hashedPassword = await bcrypt.hash('password123', 10);

    const user = await prisma.user.create({
        data: {
            username: 'admin',
            password_hash: hashedPassword,
            language: 'en',
        },
    });

    // Create a session for the user
    await prisma.userSession.create({
        data: {
            expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 1 week from now
            user_id: user.id,
        },
    });

    console.log('Seeding completed!');
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
