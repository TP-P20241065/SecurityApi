-- CreateTable
CREATE TABLE "users" (
    "id" SERIAL NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "username" VARCHAR(50) NOT NULL,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "email" VARCHAR(100) NOT NULL,
    "headquarter" INTEGER,
    "permissions" JSONB,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_active" BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "units" (
    "id" SERIAL NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "car_plate" VARCHAR(10) NOT NULL,
    "driver_id" INTEGER NOT NULL,

    CONSTRAINT "units_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "drivers" (
    "id" SERIAL NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "last_name" VARCHAR(100) NOT NULL,
    "dni" INTEGER NOT NULL,
    "image" VARCHAR(255),
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "drivers_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "cameras" (
    "id" SERIAL NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "name" VARCHAR(100),
    "location" VARCHAR(255),
    "unit_id" INTEGER,

    CONSTRAINT "cameras_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "reports" (
    "id" SERIAL NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "address" VARCHAR(255),
    "incident" VARCHAR(255),
    "tracking_link" VARCHAR(255),
    "image" VARCHAR(255) NOT NULL,
    "unit_id" INTEGER,

    CONSTRAINT "reports_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "users_email_key" ON "users"("email");

-- AddForeignKey
ALTER TABLE "units" ADD CONSTRAINT "units_driver_id_fkey" FOREIGN KEY ("driver_id") REFERENCES "drivers"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "cameras" ADD CONSTRAINT "cameras_unit_id_fkey" FOREIGN KEY ("unit_id") REFERENCES "units"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "reports" ADD CONSTRAINT "reports_unit_id_fkey" FOREIGN KEY ("unit_id") REFERENCES "units"("id") ON DELETE SET NULL ON UPDATE CASCADE;
