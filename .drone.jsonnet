local name = 'grocy';
local version = '4.5.0';
local php = '8.3.36-fpm-bookworm';
local nginx = '1.24.0';
local platform = '26.08.01';
local platform_image(distro) = 'syncloud/platform-' + distro + ':' + platform;
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
             image: 'debian:bookworm-slim',
             commands: [
               './download.sh ' + version,
             ],
           },
           {
             name: 'cli',
             image: 'golang:1.23',
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
             name: 'nginx test',
             image: platform_image('buster'),
             commands: [
               './nginx/test.sh',
             ],
           },
           {
             name: 'php',
             image: 'php:' + php,
             commands: [
               './php/build.sh',
             ],
           },
           {
             name: 'php test',
             image: platform_image('buster'),
             commands: [
               './php/test.sh',
             ],
           },
           {
             name: 'package',
             image: 'debian:bookworm-slim',
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
