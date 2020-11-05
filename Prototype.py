import json
import sys
import requests
#import schedule
import datetime
import time
import mysql.connector
from pathlib import Path

baris = (Path(__file__).stem)
nama = str(baris)
db = mysql.connector.connect(
    host="xxx",
    user="xxx",
    passwd="xxx",
    database="xxx"
    )

mycursor_pembayaran = db.cursor()
mycursor_pembayaran.execute("SELECT pembayaran FROM autobuy WHERE nomor = "+nama+" ")
myresult_pembayaran = mycursor_pembayaran.fetchone()
for pembayaran_ in myresult_pembayaran:
    pembayaran = str(pembayaran_)
    
mycursor_telegram = db.cursor()
mycursor_telegram.execute("SELECT telegram FROM autobuy WHERE nomor = "+nama+" ")
myresult_telegram = mycursor_telegram.fetchone()
for telegram_ in myresult_telegram:    
    bot_chatID_notif = str(telegram_)
    
mycursor_pid = db.cursor()
mycursor_pid.execute("SELECT product FROM autobuy WHERE nomor = "+nama+" ")
myresult_pid = mycursor_pid.fetchone()
for pid_ in myresult_pid:   
    product_id = str(pid_)
    
mycursor_cookie = db.cursor()
mycursor_cookie.execute("SELECT cookie FROM autobuy WHERE nomor = "+nama+" ")
myresult_cookie = mycursor_cookie.fetchone()
for cookie_ in myresult_cookie:    
    cookie = str(cookie_)

shipper_product_id = "999"
shipper_id = "999"
shop_id = "5433599"
warehouse_id = "3839604"
nama_produk = "xxx"
notif_pembayaran_tobotdope = "Pembayaran "+nama+" Berhasil"
sys.setrecursionlimit(10000)
url = "https://gql.tokopedia.com/"
payload = "{\"operationName\":\"AddToCart\",\"variables\":{\"productID\":"+product_id+",\"shopID\":"+shop_id+",\"quantity\":1},\"query\":\"mutation AddToCart($productID: Int!, $shopID: Int!, $quantity: Int!) {\\n  add_to_cart(productID: $productID, shopID: $shopID, quantity: $quantity) {\\n    error_message\\n    status\\n    data {\\n      success\\n      message\\n      product_id\\n      cart_id\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"
headers = {
  'Host': 'gql.tokopedia.com',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Content-Type': 'application/json',
  'X-Tkpd-Lite-Service': 'zeus',
  'X-Source': 'tokopedia-lite',
  'Origin': 'https://www.tokopedia.com',
  'Referer': 'https://www.tokopedia.com/?tab=wishlist&viewall=true',
  'Cookie': cookie  
}
headers_checkout = {
  'Host': 'gql.tokopedia.com',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Content-Type': 'application/json',
  'X-Tkpd-Lite-Service': 'zeus',
  'X-Device': 'default_v3',
  'X-TKPD-AKAMAI': 'checkout',
  'X-Source': 'tokopedia-lite',
  'Origin': 'https://www.tokopedia.com',
  'Referer': 'https://www.tokopedia.com/cart/shipment',
  'Cookie': cookie
}
headers_pay = {
  'Host': 'pay.tokopedia.com',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'https://pay.tokopedia.com',
  'Referer': 'https://pay.tokopedia.com/v2/payment?back_url=&device=default_v3&src=iframe',
  'Cookie': cookie

}
print("starting autobuy "+nama+" ")
bot_message_autobuy = ("autobuy "+nama+" berhasil")
bot_token = '1173569479:AAGO5fis0KVujrxhmU-xKq_ME8PYZV3aXQM'
bot_chatID = '958824199'
send_text_autobuy = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message_autobuy
count=1
def main():
    global count
    now = datetime.datetime.now()
    response = requests.request("POST", url, headers=headers, data = payload)
    respon = json.loads(response.text)
    result = (respon["data"]["add_to_cart"]["error_message"][0])
    cart = (respon["data"]["add_to_cart"]["data"]["cart_id"])
    payload_update_cart = "{\"operationName\":\"update_cart_items\",\"variables\":{\"lang\":\"id\",\"carts\":[{\"cart_id\":\""+cart+"\",\"quantity\":1,\"notes\":\"\"}]},\"query\":\"mutation update_cart_items(\x24lang: String, \x24carts: [ParamsCartUpdateCartV2Type]) {\\n  update_cart_v2(lang: \x24lang, carts: \x24carts) {\\n    error_message\\n    status\\n    data {\\n      error\\n      status\\n      goto\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"
    payload_shipment_address = "{\"operationName\":\"shipment_address_form\",\"variables\":{\"params\":{\"lang\":\"id\",\"is_ocs\":false}},\"query\":\"query shipment_address_form(\x24params: ShipmentAddressFormParams) {\\n  shipment_address_form(params: \x24params) {\\n    status\\n    data {\\n      hashed_email\\n      tickers {\\n        id\\n        message\\n        page\\n        __typename\\n      }\\n      open_prerequisite_site\\n      errors\\n      error_code\\n      is_multiple\\n      is_coupon_active\\n      is_one_tab_promo\\n      group_address {\\n        errors\\n        user_address {\\n          address_id\\n          address_name\\n          address\\n          postal_code\\n          phone\\n          receiver_name\\n          status\\n          country\\n          province_id\\n          province_name\\n          city_id\\n          city_name\\n          district_id\\n          district_name\\n          address_2\\n          latitude\\n          longitude\\n          corner_id\\n          __typename\\n        }\\n        group_shop {\\n          errors\\n          promo_codes\\n          shop {\\n            gold_merchant {\\n              is_gold\\n              is_gold_badge\\n              gold_merchant_logo_url\\n              __typename\\n            }\\n            official_store {\\n              is_official\\n              os_logo_url\\n              __typename\\n            }\\n            shop_id\\n            user_id\\n            shop_name\\n            shop_image\\n            shop_url\\n            shop_status\\n            is_gold\\n            is_gold_badge\\n            is_official\\n            is_free_returns\\n            address_id\\n            postal_code\\n            latitude\\n            longitude\\n            district_id\\n            district_name\\n            origin\\n            address_street\\n            province_id\\n            city_id\\n            city_name\\n            province_name\\n            country_name\\n            is_allow_manage\\n            shop_domain\\n            __typename\\n          }\\n          cart_string\\n          shipping_id\\n          sp_id\\n          rates_id\\n          dropshipper {\\n            name\\n            telp_no\\n            __typename\\n          }\\n          is_insurance\\n          is_cod_available\\n          is_order_priority\\n          shop_shipments {\\n            ship_id\\n            ship_name\\n            ship_code\\n            ship_logo\\n            ship_prods {\\n              ship_prod_id\\n              ship_prod_name\\n              ship_group_name\\n              ship_group_id\\n              minimum_weight\\n              additional_fee\\n              __typename\\n            }\\n            is_dropship_enabled\\n            __typename\\n          }\\n          products {\\n            errors\\n            cart_id\\n            product_id\\n            product_alias\\n            sku\\n            campaign_id\\n            product_name\\n            product_price_fmt\\n            trade_in_info {\\n              is_valid_trade_in\\n              new_device_price\\n              new_device_price_fmt\\n              old_device_price\\n              old_device_price_fmt\\n              __typename\\n            }\\n            product_price\\n            product_original_price\\n            product_price_original_fmt\\n            is_slash_price\\n            wholesale_price {\\n              qty_min_fmt\\n              qty_max_fmt\\n              qty_min\\n              qty_max\\n              prd_prc\\n              prd_prc_fmt\\n              __typename\\n            }\\n            product_wholesale_price\\n            product_wholesale_price_fmt\\n            product_weight_fmt\\n            product_weight\\n            product_condition\\n            product_url\\n            product_returnable\\n            product_is_free_returns\\n            free_returns {\\n              is_freereturns\\n              free_returns_logo\\n              __typename\\n            }\\n            product_is_preorder\\n            product_preorder {\\n              duration_text\\n              duration_day\\n              duration_unit_code\\n              duration_unit_text\\n              duration_value\\n              __typename\\n            }\\n            product_cashback\\n            product_min_order\\n            product_invenage_value\\n            product_switch_invenage\\n            currency_rate\\n            product_price_currency\\n            product_image_src_100_square\\n            product_all_images\\n            product_notes\\n            product_quantity\\n            product_menu_id\\n            product_finsurance\\n            product_fcancel_partial\\n            product_shipment {\\n              shipment_id\\n              __typename\\n            }\\n            product_shipment_mapping {\\n              shipment_id\\n              shipping_ids\\n              __typename\\n            }\\n            product_cat_id\\n            product_catalog_id\\n            product_status\\n            product_tracker_data {\\n              attribution\\n              tracker_list_name\\n              __typename\\n            }\\n            product_category\\n            product_total_weight\\n            product_total_weight_fmt\\n            purchase_protection_plan_data {\\n              protection_available\\n              protection_type_id\\n              protection_price_per_product\\n              protection_price\\n              protection_title\\n              protection_subtitle\\n              protection_link_text\\n              protection_link_url\\n              protection_opt_in\\n              protection_checkbox_disabled\\n              __typename\\n            }\\n            product_variants {\\n              parent_id\\n              default_child\\n              is_enabled\\n              stock\\n              __typename\\n            }\\n            warehouse_id\\n            __typename\\n          }\\n          is_fulfillment_service\\n          warehouse {\\n            warehouse_id\\n            partner_id\\n            shop_id\\n            warehouse_name\\n            district_id\\n            district_name\\n            city_id\\n            city_name\\n            province_id\\n            province_name\\n            status\\n            postal_code\\n            is_default\\n            latlon\\n            latitude\\n            longitude\\n            email\\n            address_detail\\n            country_name\\n            is_fulfillment\\n            __typename\\n          }\\n          vehicle_leasing {\\n            application_id\\n            dp_price\\n            booking_fee\\n            total_price\\n            product_id\\n            dealer_id\\n            multifinance_name\\n            is_leasing_product\\n            is_allow_checkout\\n            error_message\\n            __typename\\n          }\\n          has_promo_list\\n          __typename\\n        }\\n        sort_key\\n        __typename\\n      }\\n      kero_token\\n      kero_discom_token\\n      kero_unix_time\\n      enable_partial_cancel\\n      donation {\\n        Title\\n        Nominal\\n        Description\\n        __typename\\n      }\\n      is_one_click_shipment\\n      is_robinhood\\n      is_blackbox\\n      promo_suggestion {\\n        cta\\n        cta_color\\n        is_visible\\n        promo_code\\n        text\\n        __typename\\n      }\\n      autoapply {\\n        success\\n        code\\n        is_coupon\\n        discount_amount\\n        title_description\\n        message_success\\n        promo_id\\n        __typename\\n      }\\n      cod {\\n        is_cod\\n        counter_cod\\n        __typename\\n      }\\n      message {\\n        message_info\\n        message_link\\n        message_logo\\n        __typename\\n      }\\n      egold_attributes {\\n        eligible\\n        is_tiering\\n        tier_data {\\n          minimum_total_amount\\n          minimum_amount\\n          maximum_amount\\n          basis_amount\\n          __typename\\n        }\\n        range {\\n          min\\n          max\\n          __typename\\n        }\\n        message {\\n          title_text\\n          sub_text\\n          ticker_text\\n          tooltip_text\\n          __typename\\n        }\\n        __typename\\n      }\\n      autoapply_stack {\\n        global_success\\n        success\\n        promo_code_id\\n        discount_amount\\n        cashback_wallet_amount\\n        cashback_advocate_referral_amount\\n        cashback_voucher_description\\n        clashing_info_detail {\\n          clash_message\\n          clash_reason\\n          is_clashed_promos\\n          options {\\n            voucher_orders {\\n              cart_id\\n              code\\n              shop_name\\n              potential_benefit\\n              promo_name\\n              unique_id\\n              __typename\\n            }\\n            __typename\\n          }\\n          __typename\\n        }\\n        tracking_details {\\n          product_id\\n          promo_codes_tracking\\n          promo_details_tracking\\n          __typename\\n        }\\n        codes\\n        title_description\\n        message {\\n          color\\n          state\\n          text\\n          __typename\\n        }\\n        invoice_description\\n        gateway_id\\n        is_coupon\\n        coupon_description\\n        voucher_orders {\\n          address_id\\n          code\\n          success\\n          unique_id\\n          cart_id\\n          type\\n          cashback_wallet_amount\\n          discount_amount\\n          title_description\\n          invoice_description\\n          message {\\n            state\\n            color\\n            text\\n            __typename\\n          }\\n          is_po\\n          shop_id\\n          __typename\\n        }\\n        __typename\\n      }\\n      global_coupon_attr {\\n        description\\n        quantity_label\\n        __typename\\n      }\\n      is_show_onboarding\\n      is_hide_courier_name\\n      is_new_buyer\\n      disabled_features\\n      donation_checkbox_status\\n      promo {\\n        last_apply {\\n          code\\n          data {\\n            codes\\n            discount_amount\\n            is_coupon\\n            title_description\\n            discount_amount\\n            cashback_wallet_amount\\n            message {\\n              state\\n              text\\n              __typename\\n            }\\n            tracking_details {\\n              product_id\\n              promo_codes_tracking\\n              promo_details_tracking\\n              __typename\\n            }\\n            voucher_orders {\\n              code\\n              success\\n              cart_id\\n              shop_id\\n              order_id\\n              unique_id\\n              message {\\n                state\\n                text\\n                __typename\\n              }\\n              __typename\\n            }\\n            additional_info {\\n              usage_summaries {\\n                description\\n                type\\n                amount_str\\n                amount\\n                __typename\\n              }\\n              message_info {\\n                message\\n                detail\\n                __typename\\n              }\\n              error_detail {\\n                message\\n                __typename\\n              }\\n              __typename\\n            }\\n            __typename\\n          }\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    error_message\\n    __typename\\n  }\\n}\\n\"}"
    if "berhasil" in result :
        start_time = time.time()
        print(respon["data"]["add_to_cart"]["error_message"][0])
        print(now.strftime('%H:%M:%S.%f'))
        response_update_cart = requests.request("POST", url, headers=headers, data = payload_update_cart)
        respon_update_cart = json.loads(response_update_cart.text)
        response_shipment_address = requests.request("POST", url, headers=headers, data = payload_shipment_address)
        respon_shipment_address = json.loads(response_shipment_address.text)      
        token = (respon_shipment_address["data"]["shipment_address_form"]["data"]["kero_token"])        
        result_ut = (respon_shipment_address["data"]["shipment_address_form"]["data"]["kero_unix_time"])
        ut = str(result_ut)
        result_price = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["group_shop"][0]["products"][0]["product_price"])
        price = str(result_price)
        result_district = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["user_address"]["district_id"])
        district = str(result_district)
        postal = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["user_address"]["postal_code"])
        address_2 = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["user_address"]["address_2"])
        result_address_id = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["user_address"]["address_id"])
        address_id = str(result_address_id)
        result_district_shop = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["group_shop"][0]["shop"]["district_id"])
        district_shop = str(result_district_shop)
        postal_shop = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["group_shop"][0]["shop"]["postal_code"])
        latitude_shop = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["group_shop"][0]["shop"]["latitude"])
        longitude_shop = (respon_shipment_address["data"]["shipment_address_form"]["data"]["group_address"][0]["group_shop"][0]["shop"]["longitude"])             
        payload_rates = "{\"operationName\":\"RatesV3Query\",\"variables\":{\"input\":{\"spids\":\""+shipper_product_id+"\",\"shop_id\":\""+shop_id+"\",\"origin\":\""+district_shop+"|"+postal_shop+"|"+latitude_shop+","+longitude_shop+"\",\"weight\":\"0.2\",\"token\":\""+token+"\",\"ut\":\""+ut+"\",\"from\":\"client\",\"type\":\"default_v3\",\"service\":\"regular,nextday\",\"insurance\":\"1\",\"product_insurance\":\"1\",\"cat_id\":\"1845\",\"order_value\":\""+price+"\",\"lang\":\"id\",\"pdp\":\"0\",\"user_history\":-1,\"destination\":\""+district+"|"+postal+"|"+address_2+"\",\"vehicle_leasing\":0,\"address_id\":\""+address_id+"\",\"preorder\":0,\"is_blackbox\":0,\"psl_code\":\"\",\"products\":\"[{\\\"product_id\\\":,\\\"is_free_shipping\\\":true}]\"}},\"query\":\"query RatesV3Query(\x24input: OngkirRatesV3Input!) {\\n  ratesV3(input: \x24input) {\\n    ratesv3 {\\n      id\\n      rates_id\\n      type\\n      services {\\n        service_name\\n        service_id\\n        service_order\\n        status\\n        range_price {\\n          min_price\\n          max_price\\n          __typename\\n        }\\n        etd {\\n          min_etd\\n          max_etd\\n          __typename\\n        }\\n        texts {\\n          text_range_price\\n          text_etd\\n          text_notes\\n          text_service_notes\\n          text_price\\n          text_service_desc\\n          __typename\\n        }\\n        products {\\n          shipper_name\\n          shipper_id\\n          shipper_product_id\\n          shipper_product_name\\n          shipper_product_desc\\n          shipper_weight\\n          promo_code\\n          is_show_map\\n          status\\n          recommend\\n          checksum\\n          ut\\n          price {\\n            price\\n            formatted_price\\n            __typename\\n          }\\n          etd {\\n            min_etd\\n            max_etd\\n            __typename\\n          }\\n          texts {\\n            text_range_price\\n            text_etd\\n            text_notes\\n            text_service_notes\\n            text_price\\n            text_service_desc\\n            __typename\\n          }\\n          insurance {\\n            insurance_price\\n            insurance_type\\n            insurance_type_info\\n            insurance_used_type\\n            insurance_used_info\\n            insurance_used_default\\n            insurance_actual_price\\n            insurance_pay_type\\n            __typename\\n          }\\n          error {\\n            error_id\\n            error_message\\n            __typename\\n          }\\n          cod {\\n            is_cod_available\\n            cod_text\\n            cod_price\\n            formatted_price\\n            __typename\\n          }\\n          features {\\n            ontime_delivery_guarantee {\\n              available\\n              value\\n              text_label\\n              text_detail\\n              icon_url\\n              url_detail\\n              __typename\\n            }\\n            __typename\\n          }\\n          __typename\\n        }\\n        error {\\n          error_id\\n          error_message\\n          __typename\\n        }\\n        is_promo\\n        cod {\\n          is_cod\\n          cod_text\\n          __typename\\n        }\\n        order_priority {\\n          is_now\\n          price\\n          formatted_price\\n          inactive_message\\n          available_label\\n          static_messages {\\n            duration_message\\n            checkbox_message\\n            warningbox_message\\n            fee_message\\n            pdp_message\\n            __typename\\n          }\\n          __typename\\n        }\\n        __typename\\n      }\\n      recommendations {\\n        service_name\\n        shipping_id\\n        shipping_product_id\\n        price {\\n          price\\n          formatted_price\\n          __typename\\n        }\\n        etd {\\n          min_etd\\n          max_etd\\n          __typename\\n        }\\n        texts {\\n          text_range_price\\n          text_etd\\n          text_notes\\n          text_service_notes\\n          text_price\\n          text_service_desc\\n          __typename\\n        }\\n        insurance {\\n          insurance_price\\n          insurance_type\\n          insurance_type_info\\n          insurance_used_type\\n          insurance_used_info\\n          insurance_used_default\\n          insurance_actual_price\\n          insurance_pay_type\\n          __typename\\n        }\\n        error {\\n          error_id\\n          error_message\\n          __typename\\n        }\\n        __typename\\n      }\\n      info {\\n        cod_info {\\n          failed_message\\n          __typename\\n        }\\n        blackbox_info {\\n          text_info\\n          __typename\\n        }\\n        __typename\\n      }\\n      promo_stacking {\\n        is_promo\\n        promo_code\\n        title\\n        shipper_id\\n        shipper_product_id\\n        shipper_name\\n        shipper_desc\\n        promo_detail\\n        benefit_desc\\n        point_change\\n        user_point\\n        promo_tnc_html\\n        shipper_disable_text\\n        service_id\\n        __typename\\n      }\\n      error {\\n        error_id\\n        error_message\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"
        response_rates = requests.request("POST", url, headers=headers, data = payload_rates)
        respon_rates = json.loads(response_rates.text)       
        rates_id = (respon_rates["data"]["ratesV3"]["ratesv3"]["rates_id"])
        checksum = (respon_rates["data"]["ratesV3"]["ratesv3"]["services"][0]["products"][0]["checksum"])
        ut_checksum = (respon_rates["data"]["ratesV3"]["ratesv3"]["services"][0]["products"][0]["ut"])
        payload_checkout = "{\"operationName\":\"checkout\",\"variables\":{\"checkoutParams\":{\"carts\":{\"has_promo_stacking\":true,\"is_donation\":0,\"has_insurance_product\":false,\"leasing_id\":0,\"promos\":[],\"data\":[{\"address_id\":"+address_id+",\"shop_products\":[{\"shop_id\":"+shop_id+",\"product_data\":[{\"product_id\":"+product_id+",\"is_ppp\":false}],\"is_preorder\":0,\"warehouse_id\":"+warehouse_id+",\"finsurance\":1,\"is_dropship\":0,\"is_order_priority\":0,\"shipping_info\":{\"shipping_id\":"+shipper_id+",\"sp_id\":"+shipper_product_id+",\"rates_id\":\""+rates_id+"\",\"ut\":\""+ut_checksum+"\",\"checksum\":\""+checksum+"\",\"rates_feature\":{\"ontime_delivery_guarantee\":{\"available\":false,\"duration\":0,\"text_detail\":\"\",\"text_label\":\"\",\"icon_url\":\"\",\"url_detail\":\"\",\"url_text\":\"\"}}},\"promos\":[],\"dropship_data\":{\"name\":\"\",\"telp_no\":\"\"}}]}]},\"profile\":\"TKPD_DEFAULT\",\"is_one_click_shipment\":\"false\",\"is_cod\":false}},\"query\":\"mutation checkout($checkoutParams: CheckoutParams) {\\n  checkout(carts: $checkoutParams) {\\n    header {\\n      messages\\n      process_time\\n      reason\\n      error_code\\n      __typename\\n    }\\n    data {\\n      success\\n      error\\n      message\\n      data {\\n        redirect_url\\n        callback_url\\n        query_string\\n        parameter {\\n          merchant_code\\n          profile_code\\n          customer_id\\n          customer_name\\n          customer_email\\n          customer_msisdn\\n          transaction_id\\n          transaction_date\\n          gateway_code\\n          pid\\n          nid\\n          bid\\n          user_defined_value\\n          amount\\n          currency\\n          language\\n          signature\\n          payment_metadata\\n          merchant_type\\n          device_info {\\n            device_name\\n            device_version\\n            __typename\\n          }\\n          __typename\\n        }\\n        product_list {\\n          id\\n          price\\n          quantity\\n          name\\n          __typename\\n        }\\n        payment_type\\n        price_validation {\\n          is_updated\\n          message {\\n            title\\n            desc\\n            action\\n            __typename\\n          }\\n          tracker_data {\\n            product_changes_type\\n            campaign_type\\n            product_ids\\n            __typename\\n          }\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    error_reporter {\\n      eligible\\n      texts {\\n        submit_title\\n        submit_description\\n        submit_button\\n        cancel_button\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"        
        def checkout():
            global count
            response_checkout  = requests.request("POST", url, headers=headers_checkout, data = payload_checkout)
            respon_checkout = json.loads(response_checkout.text)
            success = (respon_checkout["data"]["checkout"]["data"]["success"])
            if success == 1:
                payload_query_string = (respon_checkout["data"]["checkout"]["data"]["data"]["query_string"])
                transaction_id = (respon_checkout["data"]["checkout"]["data"]["data"]["parameter"]["transaction_id"])
                bid = (respon_checkout["data"]["checkout"]["data"]["data"]["parameter"]["bid"])
                url_pay = "https://pay.tokopedia.com/v3/payment/json?transactionId="+transaction_id+""
                response_pay = requests.request("POST", url_pay, headers=headers_pay, data = payload_query_string)
                respon_pay = json.loads(response_pay.text)
                sig = (respon_pay["data"]["signatureInfo"]["basic"])
                ksig = (respon_pay["data"]["signatureInfo"]["kredivo"])
                result_amount = (respon_pay["data"]["amount"])
                amount = str(result_amount)
                result_user = (respon_pay["data"]["paymentInfo"]["userDefineValue"]["user_id"])
                user = str(result_user)
                profile = (respon_pay["data"]["paymentInfo"]["profileCode"])        
                url_confirm = "https://pay.tokopedia.com/v2/payment/confirm/"+pembayaran+""
                payload_confirm = "back_url=https%3A//www.tokopedia.com/cart&bank_code=&bid="+bid+"&cfee=0&customer_name=&gateway_code="+pembayaran+"&gateways=&history_state=0&is_combine_va=false&is_mobile=false&is_quickpay=false&is_topup=false&is_use_cash_points=0&is_use_ovo=0&is_use_phoenix=0&is_use_saldo=0&is_use_saldopenghasilan=0&kfee=0&ksig="+ksig+"&merchant_code=tokopedia&merchant_id=1&partial_deposit_pass=&payment_amount="+amount+"&phoenix_conversion_rate=0%3A0&profile_code="+profile+"&signature="+sig+"&topup_amount=0&topup_fee=0&transaction_id="+transaction_id+"&user_id="+user+"&voucher_code="
                response_confirm = requests.request("POST", url_confirm, headers=headers_pay, data = payload_confirm)
                print("--- %s seconds ---" % (time.time() - start_time))
                respon_confirm = json.loads(response_confirm.text)        
                payload_notif = "{\"operationName\":\"PaymentListQuery\",\"variables\":{\"lang\":\"id\",\"cursor\":\"\",\"perPage\":10},\"query\":\"query PaymentListQuery(\x24lang: String, \x24cursor: String, \x24perPage: Int) {\\n  paymentList(lang: \x24lang, cursor: \x24cursor, perPage: \x24perPage) {\\n    has_next_page\\n    last_cursor\\n    payment_list {\\n      transaction_id\\n      transaction_date\\n      transaction_expire\\n      merchant_code\\n      payment_amount\\n      invoice_url\\n      product_name\\n      product_img\\n      gateway_name\\n      gateway_img\\n      payment_code\\n      is_va\\n      is_klikbca\\n      bank_img\\n      user_bank_account {\\n        acc_no\\n        acc_name\\n        bank_id\\n        __typename\\n      }\\n      dest_bank_account {\\n        acc_no\\n        acc_name\\n        bank_id\\n        __typename\\n      }\\n      show_upload_button\\n      show_edit_transfer_button\\n      show_edit_klikbca_button\\n      show_cancel_button\\n      show_help_page\\n      ticker_message\\n      app_link\\n      how_to_pay_url\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}"
                response_notif = requests.request("POST", url, headers=headers, data = payload_notif)
                respon_notif = json.loads(response_notif.text)        
                result_jumlah = (respon_notif["data"]["paymentList"]["payment_list"][0]["payment_amount"])
                jumlah = str(result_jumlah)
                result_va = (respon_notif["data"]["paymentList"]["payment_list"][0]["gateway_name"])
                va = str(result_va)
                result_nomor_va = (respon_notif["data"]["paymentList"]["payment_list"][0]["payment_code"])
                bot_message_notif = "-DopeLink-\n[[CHECKOUT BERHASIL]]\n     !SEGERA BAYAR!\n\n"+va+"\nJumlah : "+jumlah+"\n \U0001F447 \U0001F447 \U0001F447 \U0001F447 \U0001F447"
                bot_message_notif_va = ""+result_nomor_va+""
                send_text_notif = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_notif + '&parse_mode=Markdown&text=' + bot_message_notif
                send_text_notif_va = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_notif + '&parse_mode=Markdown&text=' + bot_message_notif_va
                response_bot_notif = requests.get(send_text_notif)
                response_bot_notif_va = requests.get(send_text_notif_va)
                response_bot_autobuy = requests.get(send_text_autobuy)
                print("checkout berhasil")                
            else :
                count+=1
                error = (respon_checkout["data"]["checkout"]["data"]["error"])
                print(error,count)
                checkout()
        checkout()        
    else:
        print(now.strftime('%H:%M:%S.%f'),respon["data"]["add_to_cart"]["error_message"][0])
        print('percobaan','(',count,')')
        count+=1
        main()
main()
x = datetime.datetime.now()
tanggal = (x.strftime("%d/%m/%Y"))
def main2():
    global count
    payload_notif_pembayaran = "{\"operationName\":\"OrderList\",\"variables\":{\"EndDate\":\""+tanggal+"\",\"orderCategory\":\"MARKETPLACE\",\"OrderStatus\":5,\"Page\":1,\"PerPage\":50,\"Search\":\"\",\"Sort\":\"\",\"StartDate\":\"23/05/2020\"},\"query\":\"query OrderList(\x24orderCategory: OrderCategory, \x24Page: Int, \x24PerPage: Int, \x24Search: String, \x24StartDate: String, \x24EndDate: String, \x24Sort: String, \x24OrderStatus: Int) {\\n  orders(orderCategory: \x24orderCategory, Page: \x24Page, PerPage: \x24PerPage, Search: \x24Search, StartDate: \x24StartDate, EndDate: \x24EndDate, Sort: \x24Sort, OrderStatus: \x24OrderStatus) {\\n    categoryName\\n    category\\n    id\\n    createdAt\\n    status\\n    statusColor\\n    statusStr\\n    paymentID\\n    paymentData {\\n      label\\n      value\\n      textColor\\n      backgroundColor\\n      imageUrl\\n      __typename\\n    }\\n    shopDetails {\\n      id\\n      name\\n      logo\\n      shopURL\\n      __typename\\n    }\\n    invoiceRefNum\\n    invoiceRefURL\\n    totalInvoices\\n    title\\n    items {\\n      id\\n      name\\n      imageUrl\\n      snapshotUrl\\n      price\\n      weight\\n      quantity\\n      subTotalPrice\\n      __typename\\n    }\\n    itemCount\\n    orderLabel {\\n      flag_name\\n      flag_color\\n      flag_background\\n      __typename\\n    }\\n    paymentData {\\n      label\\n      value\\n      textColor\\n      backgroundColor\\n      imageUrl\\n      __typename\\n    }\\n    actionButtons {\\n      label\\n      key\\n      buttonType\\n      uri\\n      mappingUri\\n      __typename\\n    }\\n    deadline {\\n      label\\n      text\\n      color\\n      __typename\\n    }\\n    isWaitingInvoice\\n    cartString\\n    __typename\\n  }\\n}\\n\"}"
    response_notif_pembayaran = requests.request("POST", url, headers=headers, data = payload_notif_pembayaran)
    respon_notif_pembayaran = json.loads(response_notif_pembayaran.text)
    result_notif_pembayaran = str(respon_notif_pembayaran)
    if nama_produk in result_notif_pembayaran:
        nama_barang = (respon_notif_pembayaran["data"]["orders"][0]["items"])
        for item in nama_barang:
            barang = (">{},\n".format(item["name"]))
            produk = str(barang)
        invoice = (respon_notif_pembayaran["data"]["orders"][0]["invoiceRefNum"])
        bot_message_notif_pembayaran = "-Pembayaran Berhasil-\n\nInvoice :[["+invoice+"]]\nProduk :\n "+barang+"\n \U0000270C -DopeLink- \U0000270C"
        send_text_notif_pembayaran = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID_notif + '&parse_mode=Markdown&text=' + bot_message_notif_pembayaran
        send_text_notif_pembayaran_tobotdope = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + notif_pembayaran_tobotdope
        response_notif_pembayaran = requests.get(send_text_notif_pembayaran)
        response_notif_pembayaran_tobotdope = requests.get(send_text_notif_pembayaran_tobotdope)
        print("Pembayaran "+nama+" Berhasil")
        stop = input()
    else :
        print(""+nama+" Belum dibayar","[",count,"]")
        time.sleep(1)
        count+=1
        main2()
main2()


