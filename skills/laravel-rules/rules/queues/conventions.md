# Queues (runtime)

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

The queue runtime/infrastructure: connections, retries/backoff, failed
jobs, batching, Horizon, unique/rate-limited jobs. Distinct from
[../jobs/conventions.md](../jobs/conventions.md) (the job class's
internals) and from dispatch timing/origin
([../architecture/transactions.md](../architecture/transactions.md)).

## TODO (Pass 2)

- Connection/queue configuration conventions.
- Retries, backoff, `$tries`, timeouts.
- Failed-job handling and visibility.
- Batching, unique jobs, rate limiting.
- Horizon expectations.

## Checklist

- _(to be written)_
