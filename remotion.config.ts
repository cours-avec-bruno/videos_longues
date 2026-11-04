import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
// Rendu master : H.264 haute qualité (voir docs/specs-techniques.md).
Config.setCodec('h264');
Config.setCrf(16);
