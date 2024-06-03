CREATE TABLE [knowledgebase].[Content] (
    [ID]              INT            IDENTITY (1, 1) NOT NULL,
    [DocumentId]      INT            NOT NULL,
    [Content]         NVARCHAR (MAX) NOT NULL,
    [RedactedContent] NVARCHAR (MAX) NOT NULL,
    [PageNo]          INT            CONSTRAINT [PageNo_Df] DEFAULT ((1)) NOT NULL,
    [CreatedAt]       DATETIME       NULL,
    CONSTRAINT [PK__Content__3214EC27A9D3B54B] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [DocumentID_FK1] FOREIGN KEY ([DocumentId]) REFERENCES [knowledgebase].[Document] ([ID])
);


GO

