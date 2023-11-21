import os
from config import config
from datetime import datetime
from drivers.centre_of_registers.registered_legal_entities_driver import RegisteredLegalEntitiesDriver
from drivers.centre_of_registers.unregistered_legal_entities_driver import UnregisteredLegalEntitiesDriver
from drivers.centre_of_registers.legal_entities_management_driver import LegalEntitiesManagementDriver
from drivers.centre_of_registers.legal_entities_authorized_capital_driver import LegalEntitiesAuthorizedCapitalDriver
from drivers.centre_of_registers.legal_entities_addresses_driver import LegalEntitiesAddressesDriver
from drivers.centre_of_registers.legal_entities_balance_sheets_driver import LegalEntitiesBalanceSheetsDriver
from drivers.centre_of_registers.legal_entities_profit_loss_statements_driver import LegalEntitiesProfitLossStatementsDriver
from drivers.sodra.sodra_monthly_driver import SodraMonthlyDriver
from drivers.regitra.regitra_vehicles import RegitraVehicles


if __name__ == '__main__':
    data_path = os.path.join(config.DATA_PATH, datetime.now().strftime('%Y%m%d%H%M%S'))
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    drivers = [
        RegisteredLegalEntitiesDriver().execute(data_path),
        UnregisteredLegalEntitiesDriver().execute(data_path),
        LegalEntitiesManagementDriver().execute(data_path),
        LegalEntitiesAuthorizedCapitalDriver().execute(data_path),
        LegalEntitiesAddressesDriver().execute(data_path),
        LegalEntitiesBalanceSheetsDriver().execute(data_path),
        LegalEntitiesProfitLossStatementsDriver().execute(data_path),
        SodraMonthlyDriver().execute(data_path),
        RegitraVehicles().execute(data_path),
    ]
