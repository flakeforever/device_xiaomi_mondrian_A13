#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

import extract_utils.tools
extract_utils.tools.DEFAULT_PATCHELF_VERSION = '0_18'

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/xiaomi/mondrian',
    'hardware/qcom-caf/sm8450',
    'hardware/qcom-caf/wlan',
    'hardware/xiaomi',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.dpm.api@1.0',
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.dpmservice@1.0',
        'vendor.qti.hardware.dpmservice@1.1',
        'vendor.qti.hardware.qccsyshal@1.0',
        'vendor.qti.hardware.qccsyshal@1.1',
        'vendor.qti.hardware.qccvndhal@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.xiaomi.hardware.mlipay@1.0',
        'vendor.xiaomi.hardware.mlipay@1.1',
        # agm
        'libagm',
        'libagm_compress_plugin',
        'libagm_mixer_plugin',
        'libagm_pcm_plugin',
        'libagmclient',
        'libagmmixer',
        'libmisight',
        'libsndcardparser',
        'vendor.qti.hardware.AGMIPC@1.0-impl',
        'vendor.qti.hardware.AGMIPC@1.0',
        # graphservices
        'libar-acdb',
        'libar-gpr',
        'libar-gsl',
        'libar-pal',
        'libats',
        'liblx-ar_util',
        'liblx-osal',        
        # pal
        'libpalclient',
        'vendor.qti.hardware.pal@1.0-impl',
        'vendor.qti.hardware.pal@1.0',
        # primary-hal
        'audio.primary.taro',
        'libfmpal',
        'libmcs',
        'libqtigefar',
        # omx
        'libplatformconfig',
    ): lib_fixup_vendor_suffix,
    (
        'libvibrator',
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/libcamximageformatutils.so': blob_fixup()
        .replace_needed(
            'vendor.qti.hardware.display.config-V2-ndk_platform.so',
            'vendor.qti.hardware.display.config-V2-ndk.so',
        ),
    (
        'vendor/lib64/libTrueSight.so',
        'vendor/lib64/libalAILDC.so',
        'vendor/lib64/libalLDC.so',
        'vendor/lib64/libalhLDC.so',
    ): blob_fixup()
        .clear_symbol_version('AHardwareBuffer_allocate')
        .clear_symbol_version('AHardwareBuffer_describe')
        .clear_symbol_version('AHardwareBuffer_lock')
        .clear_symbol_version('AHardwareBuffer_lockPlanes')
        .clear_symbol_version('AHardwareBuffer_release')
        .clear_symbol_version('AHardwareBuffer_unlock'),
    'system_ext/lib64/libwfdmmsrc_system.so': blob_fixup()
        .add_needed('libgui_shim.so'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libbinder_shim.so')
        .add_needed('libinput_shim.so'),
    (
        'system_ext/lib/libwfdservice.so',
        'system_ext/lib64/libwfdservice.so',
    ): blob_fixup()
        .replace_needed(
            'android.media.audio.common.types-V2-cpp.so',
            'android.media.audio.common.types-V4-cpp.so',
        ),
    (
        'vendor/lib/libsdmcore.so',
        'vendor/lib64/libsdmcore.so',
    ): blob_fixup()
        .replace_needed(
            'libutils.so',
            'libutils-v33.so',
        ),
    (
        'vendor/lib/soundfx/libmisoundfx.so',
        'vendor/lib64/soundfx/libmisoundfx.so',
        'vendor/lib/hw/displayfeature.default.so',
        'vendor/lib64/hw/displayfeature.default.so',
    ): blob_fixup()
        .replace_needed(
            'libstagefright_foundation.so',
            'libstagefright_foundation-v33.so',
        ),
    (
        'vendor/bin/hw/dolbycodec2',
        'vendor/bin/hw/vendor.dolby.hardware.dms@2.0-service',
    ): blob_fixup()
        .add_needed('libstagefright_foundation-v33.so'),
    (
        'vendor/lib/c2.dolby.client.so',
        'vendor/lib64/c2.dolby.client.so',
    ): blob_fixup()
        .add_needed('libcodec2_hidl_shim.so'),
    'vendor/lib/libstagefright_softomx.so': blob_fixup()
        .add_needed('libui_shim.so'),
    (
        'vendor/lib/vendor.libdpmframework.so',
        'vendor/lib64/vendor.libdpmframework.so',
    ): blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    (
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/lib64/libqtikeymint.so',
    ): blob_fixup()
        .replace_needed(
            'android.hardware.security.keymint-V1-ndk_platform.so',
            'android.hardware.security.keymint-V1-ndk.so',
        )
        .replace_needed(
            'android.hardware.security.secureclock-V1-ndk_platform.so',
            'android.hardware.security.secureclock-V1-ndk.so',
        )
        .replace_needed(
            'android.hardware.security.sharedsecret-V1-ndk_platform.so',
            'android.hardware.security.sharedsecret-V1-ndk.so',
        )
        .add_needed('android.hardware.security.rkp-V1-ndk.so'),
    # 'vendor/bin/hw/vendor.qti.hardware.display.composer-service': blob_fixup()
    #     .replace_needed(
    #         'vendor.qti.hardware.display.config-V5-ndk_platform.so', 
    #         'vendor.qti.hardware.display.config-V5-ndk.so'
    #     ),
    'vendor/bin/qcc-trd': blob_fixup()
        .replace_needed(
            'libgrpc++_unsecure.so', 
            'libgrpc++_unsecure_prebuilt.so'
        ),
    'vendor/etc/init/init.embmssl_server.rc': blob_fixup()
        .regex_replace('.+interface.+\n', ''),
    'vendor/etc/qcril_database/upgrade/config/6.0_config.sql': blob_fixup()
        .regex_replace('"persist.vendor.radio.redir_party_num", "true"', '"persist.vendor.radio.redir_party_num", "false"'),
    (
        'vendor/etc/camera/mondrian_enhance_motiontuning.xml',
        'vendor/etc/camera/mondrian_motiontuning.xml',
    ): blob_fixup().regex_replace('xml=version', 'xml version'),
    'vendor/etc/camera/pureView_parameter.xml': blob_fixup()
        .regex_replace(r'=([0-9]+)>', r'="\1">'),
    # (
    #     'vendor/etc/seccomp_policy/atfwd@2.0.policy',
    #     'vendor/etc/seccomp_policy/modemManager.policy',
    #     'vendor/etc/seccomp_policy/sensors-qesdk.policy',
    #     'vendor/etc/seccomp_policy/wfdhdcphalservice.policy',
    # ): blob_fixup()
    #     .add_line_if_missing('gettid: 1'),
}  # fmt: skip

module = ExtractUtilsModule(
    'mondrian',
    'xiaomi',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()