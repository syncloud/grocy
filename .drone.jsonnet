local name = 'grocy';
local version = '4.7.1';
local php = '8.5.13-fpm-bookworm';
local nginx = '1.30.7';
local platform = '26.10.02';
local golang = '1.25';
local debian = 'bookworm-slim';
local platform_image(distro) = 'syncloud/platform-' + distro + ':' + platform;
local snapd_hold = "mkdir -p /etc/systemd/system/snapd.service.d && printf '[Service]\\nExecStartPost=/bin/sh -c \"/usr/bin/snap set system refresh.hold=2099-01-01T00:00:00Z\"\\n' > /etc/systemd/system/snapd.service.d/disable-refresh.conf && exec /sbin/init";
local playwright = 'mcr.microsoft.com/playwright:v1.59.1-jammy';
local store_publisher = 'stable-346';
local python = '3.12-slim-bookworm';
local distro_default = 'buster';
local distros = ['bookworm', 'buster'];

local build(arch, test_ui) = [{
  kind: 'pipeline',
  type: 'docker',
  name: arch,
  platform: {
    os: 'linux',
    arch: arch,
  },
  steps: [
           {
             name: 'download',
             image: 'debian:' + debian,
             commands: [
               './download.sh ' + version,
             ],
           },
           {
             name: 'cli',
             image: 'golang:' + golang,
             commands: [
               './cli/build.sh',
             ],
           },
           {
             name: 'nginx',
             image: 'nginx:' + nginx,
             commands: [
               './nginx/build.sh',
             ],
           },
           {
             name: 'php',
             image: 'php:' + php,
             commands: [
               './php/build.sh',
             ],
           },
         ] + [
           {
             name: component + ' test ' + distro,
             image: platform_image(distro),
             commands: [
               './' + component + '/test.sh',
             ],
           }
           for component in ['cli', 'nginx', 'php']
           for distro in distros
         ] + [
           {
             name: 'package',
             image: 'debian:' + debian,
             commands: [
               './package.sh ' + name + ' $DRONE_BUILD_NUMBER',
             ],
           },
         ] + [
           {
             name: 'test ' + distro,
             image: 'python:' + python,
             commands: [
               './ci/test.sh test.py ' + distro + ' ' + name,
             ],
           }
           for distro in distros

         ] + (if test_ui then [
                {
                  name: 'e2e',
                  image: playwright,
                  commands: [
                    './test/e2e/run.sh specs/01-ui.spec.ts',
                  ],
                },
                {
                  name: 'test-upgrade-prev',
                  image: 'python:' + python,
                  commands: [
                    './ci/test.sh upgrade_prev.py ' + distro_default + ' ' + name,
                  ],
                },
                {
                  name: 'e2e-before-upgrade',
                  image: playwright,
                  commands: [
                    './test/e2e/run.sh specs/02-pre-upgrade.spec.ts',
                  ],
                },
                {
                  name: 'test-upgrade',
                  image: 'python:' + python,
                  commands: [
                    './ci/test.sh upgrade.py ' + distro_default + ' ' + name,
                  ],
                },
                {
                  name: 'e2e-after-upgrade',
                  image: playwright,
                  commands: [
                    './test/e2e/run.sh specs/03-post-upgrade.spec.ts',
                  ],
                },
              ]
              else []) + [
    {
      name: 'publish',
      image: 'syncloud/store-publisher:' + store_publisher,
      environment: {
        SYNCLOUD_TOKEN: { from_secret: 'SYNCLOUD_TOKEN' },
      },
      command: ['snap', '-c', '${DRONE_BRANCH}'],
      when: {
        branch: ['stable'],
        event: ['push'],
      },
    },
    {
      name: 'artifact',
      image: 'appleboy/drone-scp:1.6.4',
      settings: {
        host: {
          from_secret: 'artifact_host',
        },
        username: 'artifact',
        key: {
          from_secret: 'artifact_key',
        },
        timeout: '2m',
        command_timeout: '2m',
        target: '/home/artifact/repo/' + name + '/${DRONE_BUILD_NUMBER}-' + arch,
        source: 'artifact/*',
        strip_components: 1,
      },
      when: {
        status: ['failure', 'success'],
        event: ['push'],
      },
    },
  ],
  trigger: {
    event: [
      'push',
    ],
  },
  services: [
    {
      name: name + '.' + distro + '.com',
      image: platform_image(distro),
      entrypoint: ['/bin/sh', '-c', snapd_hold],
      privileged: true,
      volumes: [
        {
          name: 'dbus',
          path: '/var/run/dbus',
        },
        {
          name: 'dev',
          path: '/dev',
        },
      ],
    }
    for distro in distros
  ],
  volumes: [
    {
      name: 'dbus',
      host: {
        path: '/var/run/dbus',
      },
    },
    {
      name: 'dev',
      host: {
        path: '/dev',
      },
    },
  ],
}];

build('amd64', true) +
build('arm64', false)
