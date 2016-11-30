#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

INSERT_PLAYER = "INSERT INTO player (name) values (%s)"
DELETE_ALL_PLAYER = "DELETE FROM player"
COUNT_PLAYER = "SELECT COUNT(*) FROM player"
INSERT_MATCH = "INSERT INTO MATCHES (winner, loser) values (%s, %s)"
DELETE_ALL_MATCHES = "DELETE FROM matches"
PLAYER_STANDINGS = ("SELECT  pid AS player_id, name, COALESCE(win_count, 0) AS total_win, total_match FROM "
                        "(SELECT pl.player_id AS pid, pl.name AS name, count(*) AS total_match FROM "
                                "player pl,"
                                "matches mat "
                                "WHERE mat.winner = pl.player_id "
                                "OR    mat.loser = pl.player_id "
                                "GROUP BY pl.player_id "
                                "ORDER BY pl.player_id) AS tm "
                        "LEFT JOIN "
                        "(SELECT pl.player_id AS plid, win_count FROM "
                                "player pl, "
                                "(SELECT winner, count(*) AS win_count FROM matches GROUP BY winner) AS m "
                                "WHERE m.winner = pl.player_id) AS wm "
                        "ON tm.pid = wm.plid "
                        "ORDER BY total_win desc;")

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(DELETE_ALL_MATCHES)
    conn.commit()

    cursor.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(DELETE_ALL_PLAYER)
    conn.commit()

    cursor.close()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(COUNT_PLAYER)
    result_count = cursor.fetchall()[0][0]

    cursor.close()
    conn.close()
    return result_count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(INSERT_PLAYER, (name,))
    conn.commit()

    cursor.close()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(PLAYER_STANDINGS)
    result_count = cursor.fetchall()

    cursor.close()
    conn.close()
    return result_count


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """

    conn = connect()
    cursor = conn.cursor()
    cursor.execute(INSERT_MATCH, (winner,loser,))
    conn.commit()

    cursor.close()
    conn.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM matches")
    result_count = cursor.fetchall()

    if not result_count:
        cursor.execute("SELECT * FROM player")
        result_count = cursor.fetchall()
        i = 0
        list_tup = []
        while i < len(result_count):
            tup = (result_count[i][0], result_count[i][1], result_count[i+1][0], result_count[i+1][1])
            list_tup.append(tup)
            i += 2

        cursor.close()
        conn.close()

        return list_tup
    else:
        list_standing = playerStandings()
        i = 0
        list_tup = []
        while i < len(list_standing):            
            tup = (list_standing[i][0], list_standing[i][1], list_standing[i+1][0], list_standing[i+1][1])
            list_tup.append(tup)
            i += 2

        return list_tup

if __name__ == '__main__':
    print swissPairings()
