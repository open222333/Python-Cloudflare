from argparse import ArgumentParser
from pprint import pformat
from src.logger import Log
from src.cloudflare import Record, DNSSEC, Zone
from src import LOG_LEVEL, LOG_FILE_DISABLE, CLOUDFLARE_INFO


logger = Log('MAIN')
logger.set_level(LOG_LEVEL)
if not LOG_FILE_DISABLE:
    logger.set_file_handler()
logger.set_msg_handler()

parser = ArgumentParser(description='')
args = parser.parse_args()

if __name__ == "__main__":
    for info in CLOUDFLARE_INFO:
        if info['execute']:
            try:
                zone_instance = Zone(
                    api_key=info['api_key'],
                    api_token=info['api_token'],
                    email=info['email']
                )
                with open(info['domains_txt_path'], 'r') as f:
                    domains = []
                    for domain in f.read().split('\n'):
                        if domain != '':
                            domains.append(domain)
                for domain in domains:
                    zone_response = zone_instance.create_zone(domain)
                    if zone_response:
                        if zone_response['success']:
                            logger.info(f'{domain} 域名已成功添加到 Cloudflare')

                            # 創建的域名的 Zone ID
                            zone_id = zone_response['result']['id']

                            record_instance = Record(
                                api_key=info['api_key'],
                                api_token=info['api_token'],
                                email=info['email']
                            )

                            # 添加 record
                            for record in info['records']:
                                record_response = record_instance.create_dns_record(
                                    zone_id=zone_id,
                                    record_type=record['type'],
                                    record_name=record['name'],
                                    record_content=record['content']
                                )

                                if record_response:
                                    if record_response['success']:
                                        logger.info(f'DNS 指向紀錄已成功添加:\n{pformat(record)}')
                                    else:
                                        raise RuntimeError(f'DNS 指向紀錄添加失敗:\n{pformat(record)}')
                                else:
                                    raise RuntimeError(f'DNS 指向紀錄添加失敗:\n{pformat(record)}')

                            dnssec_instance = DNSSEC(
                                record_type=record['type'],
                                record_name=record['name'],
                                record_content=record['content']
                            )
                            dnssec_id = dnssec_instance.get_dnssec_id(zone_id)
                            dnssec_response = dnssec_instance.active_dnssec(zone_id, dnssec_id)
                            if dnssec_response:
                                if dnssec_response['success']:
                                    logger.info(f'{domain} DNSSEC 已成功啟用')
                                else:
                                    raise RuntimeError(f'{domain} DNSSEC 啟用失敗 {dnssec_response}')
                            else:
                                raise RuntimeError(f'{domain} DNSSEC 啟用失敗 {dnssec_response}')
                        else:
                            raise RuntimeError(f'{domain} 域名添加失敗')
                    else:
                        raise RuntimeError(f'{domain} 域名添加失敗')
            except Exception as err:
                logger.error(err, exc_info=True)
