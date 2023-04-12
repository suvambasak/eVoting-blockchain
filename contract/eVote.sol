
pragma solidity ^0.8.0;
//SPDX-License-Identifier: MIT

contract EVoting {
    //--------------------------------Define ADMIN------------------------------------------------
    address public admin; // admin or chairperson decides voting
    
    constructor()  {
        // admindetails = Admindetails(_adminName );
        admin = msg.sender;
    }
    
    function getAdmin() public view returns (address) {
        return (admin);
    }  
    
    modifier onlyadmin() {
        // Modifier for only admin access
        require(msg.sender == admin);
        _;
    }
//---------------------------------------------------------------------------
    mapping(bytes32 => uint) public voterTimestamps; // stores the timestamp of voting for each voter
    uint public totalVotes;  // stores total no of votes
    mapping(bytes32 => bytes32) public candidate_votes; //mapping is intended to keep track of the votes cast for each candidate,
  
//----------------------------------------------------------------------   
    function vote(bytes32 _voterHash, bytes32 _candidate_email) public {
        require( block.timestamp > start_voting_time, "Election has not started yet.");
        require( block.timestamp < end_voting_time, "Election has ended.");
        //require(voter_email_ID_hash[_voterHash], "Invalid voter hash.");
        // require(!votedHashes[_voterHash], "You have already voted.");
        candidate_votes[_candidate_email] = _voterHash;
        // votedHashes[_voterEmailHash] = true;
        voterTimestamps[_voterHash] = block.timestamp;
        totalVotes++;
        //return (candidate.votes, candidate_votes[_candidate_email]);
    }

    function getCandidateVoteCount(bytes32 _candidate_hash) public view returns (uint, bytes32, uint[] memory) {
        require(block.timestamp > end_voting_time || msg.sender == admin, "Vote count not available yet.");
        bytes32 voters = candidate_votes[_candidate_hash];
        uint[] memory voteTimestamps = new uint[](voters.length);
        for (uint i = 0; i < voters.length; i++) {
            voteTimestamps[i] = voterTimestamps[voters[i]];
        }
    return (voters.length, voters, voteTimestamps);
    }
//------------------------------------------------------------------------------  
    uint256 public start_voting_time;
    uint256 public end_voting_time;

      function setVotingTime(uint _start_voting_time, uint _end_voting_time) public onlyadmin {
        require(block.timestamp < _start_voting_time, "Starting time should be in future");
        require(block.timestamp < _end_voting_time && _end_voting_time > _start_voting_time , "End time for voting  to be greater than start time");
        start_voting_time = _start_voting_time;
        end_voting_time = _end_voting_time;
        
    }

    function extendVotingTime(uint _extendTime) public onlyadmin {
        require(block.timestamp<end_voting_time, "Voting already ended");
        end_voting_time = end_voting_time + _extendTime;
    }
}
