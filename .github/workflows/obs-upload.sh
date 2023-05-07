#!/bin/sh
set -e

RELEASES='fedora:37 fedora:38'

for i in git curl xmlstarlet rpmspec
do
    if test -z "$(which "$i" || true)"
    then
        echo "The $i binary could not be found. Aborting."
        exit 1
    fi
done

BASE="$(git rev-parse --show-toplevel 2> /dev/null)"
SPECFILE="${BASE}/ungoogled-chromium.spec"
SOURCES="${BASE}/sources"

if test -z "${BASE}"
then
    echo "BASE directory could not be determined. Aborting."
    exit 1
fi

if test ! -f "${SPECFILE}"
then
    echo "${SPECFILE} must exist and be a regular file. Aborting."
    exit 1
fi

for i in OBS_API_USERNAME OBS_API_PASSWORD
do
    if test -z "$(eval echo \$${i})"
    then
        echo "$i is not in the environment. Aborting."
        exit 1
    fi
done

PROJECT="${OBS_API_PROJECT:-home:${OBS_API_USERNAME}}"

curl()
{
    for i in `seq 1 5`
    do
        {
        command curl -sS -K - "${@}" << EOF
user="${OBS_API_USERNAME}:${OBS_API_PASSWORD}"
EOF
        } && return 0 || sleep 30s
    done
    return 1
}

get_type()
{
    local TAG
    local TYPE

    TAG="$(git describe --tags --exact-match 2> /dev/null || true)"

    if test -z "${TAG}"
    then
        TYPE='development'
    else
        TYPE='production'
    fi

    echo "${TYPE}"
}

generate_obs()
{
    local ROOT="${1}"
    local i
    local release
    local version
    local url
    local filename
    local verifier
    local checksum
    local revision

    sed -r '1c%global obs 1' "${SPECFILE}" > "${ROOT}/ungoogled-chromium.spec"
    SPECFILE="${ROOT}/ungoogled-chromium.spec"

    for i in ${RELEASES}
    do
        release="${i%:*}"
        version="${i#*:}"
        rpmspec -E "%global ${release} ${version}" -P "${SPECFILE}" | sed -n -r '/^(Source|Patch)[0-9]+:/s/(Source|Patch)[0-9]+:\s*(\S+)\s*/\2/p' >> "${ROOT}/files"
    done

    printf '<services>\n' > "${ROOT}/_service"
    sort -u < "${ROOT}/files" | while read i
    do
        if echo "${i}" | grep -q -E '^https?://'
        then
            url="${i}"
            filename="${url##*/}"
            verifier="$(grep "(${filename})" "${SOURCES}" | cut -d ' ' -f 1 | tr 'A-Z' 'a-z')"
            checksum="$(grep "(${filename})" "${SOURCES}" | cut -d = -f 2 | sed 's;^ *\| *$;;g')"
            printf '%s<service name="download_url">\n' '    ' >> "${ROOT}/_service"
            printf '%s<param name="url">%s</param>\n' '        ' "${url}" >> "${ROOT}/_service"
            printf '%s</service>\n' '    ' >> "${ROOT}/_service"
            printf '%s<service name="verify_file">\n' '    ' >> "${ROOT}/_service"
            printf '%s<param name="file">%s</param>\n' '        ' "_service:download_url:${filename}" >> "${ROOT}/_service"
            printf '%s<param name="verifier">%s</param>\n' '        ' "${verifier}" >> "${ROOT}/_service"
            printf '%s<param name="checksum">%s</param>\n' '        ' "${checksum}" >> "${ROOT}/_service"
            printf '%s</service>\n' '    ' >> "${ROOT}/_service"
        elif ! echo "${i}" | grep -q -E '^depot_tools-[^.]+[.]tar[.]xz$'
        then
            cp "${BASE}/${i}" "${ROOT}"
        fi
    done
    printf '</services>\n' >> "${ROOT}/_service"

    rm -f "${ROOT}/files"
}

upload_obs()
{
    local ROOT="${1}"
    local TYPE="${2}"
    local REPOSITORY
    local PACKAGE="ungoogled-chromium-fedora"
    local FILE
    local FILENAME

    case "${TYPE}" in

        production)
            REPOSITORY="${PROJECT}"
            ;;

        development)
            REPOSITORY="${PROJECT}:testing"
            ;;

    esac

    curl "https://api.opensuse.org/source/${REPOSITORY}/${PACKAGE}" -F 'cmd=deleteuploadrev'

    curl "https://api.opensuse.org/source/${REPOSITORY}/${PACKAGE}" > "${ROOT}/directory.xml"

    xmlstarlet sel -t -v '//entry/@name' < "${ROOT}/directory.xml" | while read FILENAME
    do
        curl "https://api.opensuse.org/source/${REPOSITORY}/${PACKAGE}/${FILENAME}?rev=upload" -X DELETE
    done

    rm -f "${ROOT}/directory.xml"

    for FILE in "${ROOT}"/*
    do
        FILENAME="${FILE##*/}"
        curl "https://api.opensuse.org/source/${REPOSITORY}/${PACKAGE}/${FILENAME}?rev=upload" -T "${FILE}"
    done

    curl "https://api.opensuse.org/source/${REPOSITORY}/${PACKAGE}" -F 'cmd=commit'
}

TMP="$(mktemp -d)"
TYPE="$(get_type)"

trap 'rm -rf "${TMP}"' EXIT INT
generate_obs "${TMP}"
upload_obs "${TMP}" "${TYPE}"
