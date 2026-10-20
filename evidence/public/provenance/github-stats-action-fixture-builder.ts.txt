// The fixtures' Dataset, built the way the action builds it. The 2026-10-18 releases come from
// releases.json, since the stored day in snapshots/ predates v1.20.0.

import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import {
  buildDataset,
  loadConfig,
  mergeTrafficDays,
  readSnapshots,
  toTrafficResponse,
  type Dataset,
  type Snapshot,
  type SnapshotRelease,
  type TrafficRaw,
} from '../packages/core/src';

export const FIXTURE_TAKEN_AT = '2026-10-18T13:00:00Z';

export async function buildFixtureDataset(): Promise<Dataset> {
  const fixtures = fileURLToPath(new URL('../fixtures/', import.meta.url));
  const read = async <T>(path: string): Promise<T> => JSON.parse(await readFile(fixtures + path, 'utf8')) as T;
  const repo = 'elboletaire/manga-downloader';
  const config = await loadConfig(fixtures + 'manga-downloader.stats.yml');

  const [snapshot17, stored18] = await readSnapshots(fixtures);
  const apiReleases = await read<
    { tag_name: string; draft: boolean; prerelease: boolean; published_at: string; assets: { name: string; download_count: number }[] }[]
  >('releases.json');

  const releases: SnapshotRelease[] = apiReleases
    .filter((r) => !r.draft)
    .map((r) => ({
      tag: r.tag_name,
      publishedAt: r.published_at,
      prerelease: r.prerelease,
      assets: r.assets.map((a) => ({ name: a.name, downloads: a.download_count })),
    }));

  const snapshot18: Snapshot = { ...stored18!, takenAt: FIXTURE_TAKEN_AT, releases };

  const raw: TrafficRaw = {
    views: await read('traffic/views.json'),
    clones: await read('traffic/clones.json'),
    referrers: await read('traffic/referrers.json'),
    paths: await read('traffic/paths.json'),
  };
  const traffic = toTrafficResponse(raw);

  return buildDataset({
    repo,
    config,
    snapshots: [snapshot17!, snapshot18],
    // Synthetic sample: 18 timestamps, not the repo's stargazers (totals.stars is 271), so the stars chart ends at 18.
    stargazers: await read<string[]>('stargazers.json'),
    traffic: {
      views: mergeTrafficDays([], traffic.views),
      clones: mergeTrafficDays([], traffic.clones),
      referrers: traffic.referrers,
      paths: traffic.paths,
      asOf: '2026-10-18',
    },
    now: new Date(FIXTURE_TAKEN_AT),
  });
}
