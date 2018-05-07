from quarkchain.core import hash256, uint16, uint32, uint64, uint128, uint256, boolean
from quarkchain.core import (
    Transaction,
    PreprendedSizeBytesSerializer, PreprendedSizeListSerializer, Serializable, Address, Branch, ShardMask
)

from quarkchain.cluster.core import MinorBlock, MinorBlockHeader, RootBlock, CrossShardTransactionList


# RPCs to initialize a cluster

class Ping(Serializable):
    FIELDS = [
        ("id", PreprendedSizeBytesSerializer(4)),
        ("shardMaskList", PreprendedSizeListSerializer(4, ShardMask)),
    ]

    def __init__(self, id, shardMaskList):
        """ Empty shardMaskList means root """
        if isinstance(id, bytes):
            self.id = id
        else:
            self.id = bytes(id, "ascii")
        self.shardMaskList = shardMaskList


class Pong(Serializable):
    FIELDS = [
        ("id", PreprendedSizeBytesSerializer(4)),
        ("shardMaskList", PreprendedSizeListSerializer(4, ShardMask)),
    ]

    def __init__(self, id, shardMaskList):
        """ Empty slaveId and shardMaskList means root """
        if isinstance(id, bytes):
            self.id = id
        else:
            self.id = bytes(id, "ascii")
        self.shardMaskList = shardMaskList


class SlaveInfo(Serializable):
    FIELDS = [
        ("id", PreprendedSizeBytesSerializer(4)),
        ("ip", uint128),
        ("port", uint16),
        ("shardMaskList", PreprendedSizeListSerializer(4, ShardMask)),
    ]

    def __init__(self, id, ip, port, shardMaskList):
        if isinstance(id, bytes):
            self.id = id
        else:
            self.id = bytes(id, "ascii")
        self.ip = ip
        self.port = port
        self.shardMaskList = shardMaskList


class ConnectToSlavesRequest(Serializable):
    ''' Master instructs a slave to connect to other slaves '''
    FIELDS = [
        ("slaveInfoList", PreprendedSizeListSerializer(4, SlaveInfo)),
    ]

    def __init__(self, slaveInfoList):
        self.slaveInfoList = slaveInfoList


class ConnectToSlavesResponse(Serializable):
    ''' resultList must have the same size as salveInfoList in the request.
    Empty result means success otherwise it would a serialized error message.
    '''
    FIELDS = [
        ("resultList", PreprendedSizeListSerializer(4, PreprendedSizeBytesSerializer(4))),
    ]

    def __init__(self, resultList):
        self.resultList = resultList


# RPCs to update blockchains

# master -> slave

class AddRootBlockRequest(Serializable):
    ''' Add root block to each slave
    '''
    FIELDS = [
        ("rootBlock", RootBlock),
        ("expectSwitch", boolean),
    ]

    def __init__(self, rootBlock, expectSwitch):
        self.rootBlock = rootBlock
        self.expectSwitch = expectSwitch


class AddRootBlockResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
        ("switched", boolean),
    ]

    def __init__(self, errorCode, switched):
        self.errorCode = errorCode
        self.switched = switched


class EcoInfo(Serializable):
    ''' Necessary information for master to decide the best block to mine '''
    FIELDS = [
        ("branch", Branch),
        ("height", uint64),
        ("coinbaseAmount", uint256),
        ("difficulty", uint64),
        ("unconfirmedHeadersCoinbaseAmount", uint256)
    ]

    def __init__(self, branch, height, coinbaseAmount, difficulty, unconfirmedHeadersCoinbaseAmount):
        self.branch = branch
        self.height = height
        self.coinbaseAmount = coinbaseAmount
        self.difficulty = difficulty
        self.unconfirmedHeadersCoinbaseAmount = unconfirmedHeadersCoinbaseAmount


class GetEcoInfoListRequest(Serializable):
    FIELDS = []

    def __init__(self):
        pass


class GetEcoInfoListResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
        ("ecoInfoList", PreprendedSizeListSerializer(4, EcoInfo)),
    ]

    def __init__(self, errorCode, ecoInfoList):
        self.errorCode = errorCode
        self.ecoInfoList = ecoInfoList


class GetNextBlockToMineRequest(Serializable):
    FIELDS = [
        ("branch", Branch),
        ("address", Address),
    ]

    def __init__(self, branch, address):
        self.branch = branch
        self.address = address


class GetNextBlockToMineResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
        ("block", MinorBlock),
    ]

    def __init__(self, errorCode, block):
        self.errorCode = errorCode
        self.block = block


class AddMinorBlockRequest(Serializable):
    FIELDS = [
        ("minorBlock", MinorBlock),
    ]

    def __init__(self, minorBlock):
        self.minorBlock = minorBlock


class AddMinorBlockResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
    ]

    def __init__(self, errorCode):
        self.errorCode = errorCode


class HeadersInfo(Serializable):
    FIELDS = [
        ("branch", Branch),
        ("headerList", PreprendedSizeListSerializer(4, MinorBlockHeader)),
    ]

    def __init__(self, branch, headerList):
        self.branch = branch
        self.headerList = headerList


class GetUnconfirmedHeadersRequest(Serializable):
    FIELDS = []

    def __init__(self):
        pass


class GetUnconfirmedHeadersResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
        ("headersInfoList", PreprendedSizeListSerializer(4, HeadersInfo)),
    ]

    def __init__(self, errorCode, headersInfoList):
        self.errorCode = errorCode
        self.headersInfoList = headersInfoList


class GetTransactionCountRequest(Serializable):
    FIELDS = [
        ("address", Address),
    ]

    def __init__(self, address):
        self.address = address


class GetTransactionCountResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
        ("count", uint256),
    ]

    def __init__(self, errorCode, count):
        self.errorCode = errorCode
        self.count = count


class AddTransactionRequest(Serializable):
    FIELDS = [
        ("tx", Transaction),
    ]

    def __init__(self, tx):
        self.tx = tx


class AddTransactionResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
    ]

    def __init__(self, errorCode):
        self.errorCode = errorCode


class DownloadMinorBlockListRequest(Serializable):
    FIELDS = [
        ("minorBlockHashList", PreprendedSizeListSerializer(4, hash256)),
    ]

    def __init__(self, minorBlockHashList):
        self.minorBlockHashList = minorBlockHashList


class DownloadMinorBlockListResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
        ("minorBlockList", PreprendedSizeListSerializer(4, MinorBlock))
    ]

    def __init__(self, errorCode):
        self.errorCode = errorCode


# slave -> master

class AddMinorBlockHeaderRequest(Serializable):
    FIELDS = [
        ("minorBlockHeader", MinorBlockHeader),
    ]

    def __init__(self, minorBlockHeader):
        self.minorBlockHeader = minorBlockHeader


class AddMinorBlockHeaderResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32),
    ]

    def __init__(self, errorCode):
        self.errorCode = errorCode


# slave -> slave

class AddXshardTxListRequest(Serializable):
    FIELDS = [
        ("branch", Branch),
        ("minorBlockHash", hash256),
        ("txList", CrossShardTransactionList),
    ]

    def __init__(self, branch, minorBlockHash, txList):
        self.branch = branch
        self.minorBlockHash = minorBlockHash
        self.txList = txList


class AddXshardTxListResponse(Serializable):
    FIELDS = [
        ("errorCode", uint32)
    ]

    def __init__(self, errorCode):
        self.errorCode = errorCode


CLUSTER_OP_BASE = 128


class ClusterOp():

    # TODO: Remove cluster op base as cluster op should be indepedent to p2p op
    PING = 1 + CLUSTER_OP_BASE
    PONG = 2 + CLUSTER_OP_BASE
    CONNECT_TO_SLAVES_REQUEST = 3 + CLUSTER_OP_BASE
    CONNECT_TO_SLAVES_RESPONSE = 4 + CLUSTER_OP_BASE
    ADD_ROOT_BLOCK_REQUEST = 5 + CLUSTER_OP_BASE
    ADD_ROOT_BLOCK_RESPONSE = 6 + CLUSTER_OP_BASE
    GET_ECO_INFO_LIST_REQUEST = 7 + CLUSTER_OP_BASE
    GET_ECO_INFO_LIST_RESPONSE = 8 + CLUSTER_OP_BASE
    GET_NEXT_BLOCK_TO_MINE_REQUEST = 9 + CLUSTER_OP_BASE
    GET_NEXT_BLOCK_TO_MINE_RESPONSE = 10 + CLUSTER_OP_BASE
    GET_UNCONFIRMED_HEADERS_REQUEST = 11 + CLUSTER_OP_BASE
    GET_UNCONFIRMED_HEADERS_RESPONSE = 12 + CLUSTER_OP_BASE
    GET_TRANSACTION_COUNT_REQUEST = 13 + CLUSTER_OP_BASE
    GET_TRANSACTION_COUNT_RESPONSE = 14 + CLUSTER_OP_BASE
    ADD_TRANSACTION_REQUEST = 15 + CLUSTER_OP_BASE
    ADD_TRANSACTION_RESPONSE = 16 + CLUSTER_OP_BASE
    ADD_MINOR_BLOCK_HEADER_REQUEST = 17 + CLUSTER_OP_BASE
    ADD_MINOR_BLOCK_HEADER_RESPONSE = 18 + CLUSTER_OP_BASE
    ADD_XSHARD_TX_LIST_REQUEST = 19 + CLUSTER_OP_BASE
    ADD_XSHARD_TX_LIST_RESPONSE = 20 + CLUSTER_OP_BASE
    DOWNLOAD_MINOR_BLOCK_LIST_REQUEST = 21 + CLUSTER_OP_BASE
    DOWNLOAD_MINOR_BLOCK_LIST_RESPONSE = 22 + CLUSTER_OP_BASE
    ADD_MINOR_BLOCK_REQUEST = 23 + CLUSTER_OP_BASE
    ADD_MINOR_BLOCK_RESPONSE = 24 + CLUSTER_OP_BASE


CLUSTER_OP_SERIALIZER_MAP = {
    ClusterOp.PING: Ping,
    ClusterOp.PONG: Pong,
    ClusterOp.CONNECT_TO_SLAVES_REQUEST: ConnectToSlavesRequest,
    ClusterOp.CONNECT_TO_SLAVES_RESPONSE: ConnectToSlavesResponse,
    ClusterOp.ADD_ROOT_BLOCK_REQUEST: AddRootBlockRequest,
    ClusterOp.ADD_ROOT_BLOCK_RESPONSE: AddRootBlockResponse,
    ClusterOp.GET_ECO_INFO_LIST_REQUEST: GetEcoInfoListRequest,
    ClusterOp.GET_ECO_INFO_LIST_RESPONSE: GetEcoInfoListResponse,
    ClusterOp.GET_NEXT_BLOCK_TO_MINE_REQUEST: GetNextBlockToMineRequest,
    ClusterOp.GET_NEXT_BLOCK_TO_MINE_RESPONSE: GetNextBlockToMineResponse,
    ClusterOp.ADD_MINOR_BLOCK_REQUEST: AddMinorBlockRequest,
    ClusterOp.ADD_MINOR_BLOCK_RESPONSE: AddMinorBlockResponse,
    ClusterOp.GET_UNCONFIRMED_HEADERS_REQUEST: GetUnconfirmedHeadersRequest,
    ClusterOp.GET_UNCONFIRMED_HEADERS_RESPONSE: GetUnconfirmedHeadersResponse,
    ClusterOp.ADD_MINOR_BLOCK_HEADER_REQUEST: AddMinorBlockHeaderRequest,
    ClusterOp.ADD_MINOR_BLOCK_HEADER_RESPONSE: AddMinorBlockHeaderResponse,
    ClusterOp.ADD_XSHARD_TX_LIST_REQUEST: AddXshardTxListRequest,
    ClusterOp.ADD_XSHARD_TX_LIST_RESPONSE: AddXshardTxListResponse,
    ClusterOp.GET_TRANSACTION_COUNT_REQUEST: GetTransactionCountRequest,
    ClusterOp.GET_TRANSACTION_COUNT_RESPONSE: GetTransactionCountResponse,
    ClusterOp.ADD_TRANSACTION_REQUEST: AddTransactionRequest,
    ClusterOp.ADD_TRANSACTION_RESPONSE: AddTransactionResponse,
    ClusterOp.DOWNLOAD_MINOR_BLOCK_LIST_REQUEST: DownloadMinorBlockListRequest,
    ClusterOp.DOWNLOAD_MINOR_BLOCK_LIST_RESPONSE: DownloadMinorBlockListResponse,
}
