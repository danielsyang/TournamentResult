-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
CREATE DATABASE tournament;

CREATE TABLE player (
  player_id  SERIAL PRIMARY KEY NOT NULL,
  name  TEXT NOT NULL
);

CREATE TABLE MATCHES (
  match_id SERIAL PRIMARY KEY NOT NULL,
  winner INTEGER,
  loser INTEGER,
  FOREIGN KEY (winner) REFERENCES player(player_id),
  FOREIGN KEY (loser) REFERENCES player(player_id)
);