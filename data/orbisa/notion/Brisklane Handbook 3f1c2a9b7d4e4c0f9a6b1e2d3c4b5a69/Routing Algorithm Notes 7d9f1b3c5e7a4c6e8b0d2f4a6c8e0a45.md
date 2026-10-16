# Routing Algorithm Notes

Owner: Luca Ferretti
Last edited time: October 2, 2024 4:20 PM
Status: Active

How the Brisklane router plans last-mile routes.

## Inputs

- Stops with time windows, vehicle capacity, driver shift length.
- Live traffic from the map provider, refreshed every 10 minutes.

## Approach

1. Cluster stops by zone.
2. Solve each cluster with a time-window vehicle routing heuristic.
3. Re-optimize when a stop is added or a vehicle is late by more than 15 minutes.

## Known limits

Routes with more than 300 stops per vehicle are slow to re-optimize. Batch them overnight.
