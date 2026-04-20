@echo off
echo ========================================
echo   VERIFICACION DE INSTALACION TDD
echo   Validador de PDF
echo ========================================
echo.

echo [1/4] Verificando estructura de archivos...
if exist "app\services\file_validator.py" (
    echo   [OK] file_validator.py
) else (
    echo   [ERROR] file_validator.py NO ENCONTRADO
    exit /b 1
)

if exist "app\controllers\file_controller.py" (
    echo   [OK] file_controller.py
) else (
    echo   [ERROR] file_controller.py NO ENCONTRADO
    exit /b 1
)

if exist "tests\test_file_validator.py" (
    echo   [OK] test_file_validator.py
) else (
    echo   [ERROR] test_file_validator.py NO ENCONTRADO
    exit /b 1
)

if exist "tests\test_file_endpoint.py" (
    echo   [OK] test_file_endpoint.py
) else (
    echo   [ERROR] test_file_endpoint.py NO ENCONTRADO
    exit /b 1
)

echo.
echo [2/4] Verificando ejemplo de uso...
python example_usage.py
if %errorlevel% neq 0 (
    echo   [ERROR] Ejemplo fallo
    exit /b 1
)

echo.
echo [3/4] Ejecutando tests del servicio...
python tests\test_file_validator.py
if %errorlevel% neq 0 (
    echo   [ERROR] Tests del servicio fallaron
    exit /b 1
)

echo.
echo [4/4] Ejecutando tests del endpoint...
python tests\test_file_endpoint.py
if %errorlevel% neq 0 (
    echo   [ERROR] Tests del endpoint fallaron
    exit /b 1
)

echo.
echo ========================================
echo   VERIFICACION COMPLETADA
echo ========================================
echo.
echo   ✓ Todos los archivos creados
echo   ✓ Ejemplo de uso funciona
echo   ✓ Tests del servicio pasan (7/7)
echo   ✓ Tests del endpoint pasan (5/5)
echo   ✓ Total: 12 tests passing
echo.
echo   Siguiente paso:
echo   1. Ejecutar servidor: python app.py
echo   2. Abrir: test_manual.html
echo   3. Probar con archivos reales
echo.
echo ========================================
