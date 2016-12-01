-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
  player_id  SERIAL PRIMARY KEY NOT NULL,
  name  TEXT NOT NULL
);

CREATE TABLE matches (
  match_id SERIAL PRIMARY KEY NOT NULL,
  winner INTEGER,
  loser INTEGER,
  FOREIGN KEY (winner) REFERENCES players(player_id),
  FOREIGN KEY (loser) REFERENCES players(player_id)
);

CREATE VIEW total_matches AS
        SELECT  pl.player_id, COUNT(*) AS total_matches
        FROM players pl, matches mat
        WHERE mat.winner = pl.player_id
        OR mat.loser = pl.player_id
        GROUP BY pl.player_id
        ORDER BY pl.player_id;

CREATE VIEW total_wins AS
        SELECT pl.player_id, total_wins
        FROM players pl,
        (
          SELECT winner,count(*) AS total_wins
          FROM matches
          GROUP BY winner
        ) AS mat
        WHERE mat.winner = pl.player_id;
