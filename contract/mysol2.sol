    pragma solidity = 0.8.19;
    //SPDX-License-Identifier: MIT
    contract EVoting {
        address public admin; // admin or chairperson decides voting
        struct Admindetails {
            string adminName;             
        }
        Admindetails public admindetails;

        
        constructor()  {
            admin = msg.sender;
        }
        
        // Admin details
        function getAdmin() public view returns (address, string memory) {
        return (admin, admindetails.adminName);
        }  
        
        modifier onlyadmin() {
            // Modifier for only admin access
            require(msg.sender == admin);
            _;
        }

        //--------------------------------------
        // bytes32[] public voter_email_hashes; //array  to store the email hashes of VOTERS. 
        // bytes32[] public candidate_email_hash; // array to store the email hashes of CANDIDATES

        //mapping(bytes32 => uint) public voter_email_ID; // mapping is to store the hash values of voter email IDs 
                                                            //and indicate whether a given email ID has already voted in an election.

        //mapping(string => uint) public candidate_emailID; //purpose of this mapping is to store the candidate email IDs 
                                                                // and indicate whether a given email ID is a valid candidate in an election.

        mapping(bytes32 => bool) public votedHashes; //This mapping is  to keep track of hashed values that have been voted on, 
                                                    //with the boolean value being set to true to indicate that a particular hashed 
                                                    //value has already been voted on.

        mapping(bytes32 => bytes32[]) public candidate_votes; // mapping is intended to keep track of the votes cast for each candidate, 
                                                            //with each element in the array representing a hashed value of the vote. 
                                                            //The key of this mapping represents the candidate being voted for, 
                                                            //and the array of hashed values represents the votes cast for that candidate.

        mapping(bytes32 => uint) public voterTimestamps; // stores the timestamp of voting for each voter
        uint public totalVotes;


       //----------------------------------------------------------------- 
       
        mapping(bytes32 => bool) public candidate_emailID_hash;
      
        function addCandidate(bytes32 _candidate_email) public onlyadmin {  
            require(!candidate_emailID_hash[_candidate_email] == true, 'you have been already registered');
            candidate_emailID_hash[_candidate_email] = true;
        }
        
        mapping(bytes32 => bool) public voter_emailID_hash;

        function addVoter(bytes32 _voter_email) public onlyadmin {  
            require(!voter_emailID_hash[_voter_email] == true, 'you have been already registered');
            voter_emailID_hash[_voter_email] = true;
        }
        
        
    //  //----------------------------------------------------------------------   
        function vote(bytes32 _voterEmailHash, bytes32 _candidate_email) public {
            //require( block.timestamp > start_voting_time, "Election has not started yet.");
            //require( block.timestamp < end_voting_time, "Election has ended.");
            ////require(voter_email_ID_hash[_voterHash], "Invalid voter hash.");
            //require(!votedHashes[_voterEmailHash], "You have already voted.");
            candidate_votes[_candidate_email].push(_voterEmailHash);
            votedHashes[_voterEmailHash] = true;
            voterTimestamps[_voterEmailHash] = block.timestamp;
            totalVotes++;
            //return (candidate.votes, candidate_votes[_candidate_email]);
        
        }

        function getCandidateVoteCount(bytes32 _candidate_email) public view returns (uint, bytes32[] memory, uint[] memory) {
        require(block.timestamp > end_voting_time || msg.sender == admin, "Vote count not available yet.");
        bytes32[] memory voters = candidate_votes[_candidate_email];
        uint[] memory voteTimestamps = new uint[](voters.length);
        for (uint i = 0; i < voters.length; i++) {
            voteTimestamps[i] = voterTimestamps[voters[i]];
        }
        return (voters.length, voters, voteTimestamps);
    }


    //   //------------------------------------------------------------------------------  
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

